from collections import defaultdict
from datetime import datetime
import json, os, zstandard

# From https://github.com/Watchful1/PushshiftDumps
def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)

# From https://github.com/Watchful1/PushshiftDumps
def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)

			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line, file_handle.tell()

			buffer = lines[-1]

		reader.close()
        
# From https://github.com/Watchful1/PushshiftDumps
def write_line_zst(handle, line):
	handle.write(line.encode('utf-8'))
	handle.write("\n".encode('utf-8'))


def subset_zst(input_path: str,
               output_path: str,
               start_date: datetime=None,
               end_date: datetime=None,
               keys: list=None):

    # Create the zst handler
    handle = zstandard.ZstdCompressor().stream_writer(open(output_path, 'wb'))

    # Save the data to zst file
    with open(output_path, mode="w", newline="") as file:

        for line, file_bytes_processed in read_lines_zst(input_path):
            obj = json.loads(line)

            # Filter out comments that don't have a created_utc field
            if "created_utc" not in obj: continue
            created_utc = datetime.fromtimestamp(int(obj["created_utc"]))
            
            # Filter by date
            if created_utc < start_date: continue
            if created_utc > end_date: continue
            
            # Select the keys (if they exist)
            obj = {key: obj.get(key, "") for key in keys}
            
            # Skip if body is empty or deleted
            if obj["body"] == "" or obj["body"] == "[deleted]": continue

            # if id is in the keys, change it to link_id
            if "id" in keys:
                # Select characters after underscore
                try:
                    obj["link_id"] = obj["id"].split("_")[1]
                except:
                    obj["link_id"] = ""

            # Write the data to the zst file
            line_clean = json.dumps(obj)
            write_line_zst(handle, line_clean)
    
    print(f"Data written to {output_path}")

    return

if __name__ == "__main__":

    # Set the start and end dates
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2022, 12, 31)

    # Set the keys to keep
    keys_comments = ["link_id", "author", "created_utc", "body", "score", "ups", "downs", "controversiality", "gilded"]
    #keys_submissions = ["id", "author", "downs", "ups", "title", "num_comments", "created_utc", "selftext", "score"]

    subreddits = ["Conservative", "progressive",
                  "democrats", "Republican",
                  "NeutralPolitics", "PoliticalDiscussion", "politics"]

    for subreddit in subreddits:

        # Set the input and output paths
        input_path = f"/ata/{subreddit}/{subreddit}_comments.zst"
        output_path = f"data/{subreddit}/{subreddit}_comments_subset.zst"
        #input_path = f"data/{subreddit}/{subreddit}_submissions.zst"
        #output_path = f"data/{subreddit}/{subreddit}_submissions_subset.zst"

        # Subset the data
        subset_zst(input_path, output_path, start_date, end_date, keys_comments)