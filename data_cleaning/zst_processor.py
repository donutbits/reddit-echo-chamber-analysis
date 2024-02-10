"""
These functions were adapted from https://github.com/Watchful1/PushshiftDumps
"""

import zstandard


def read_and_decode(reader, chunk_size, max_window_size):
    chunks = []
    bytes_read = 0

    while True:
        chunk = reader.read(chunk_size)
        if not chunk:
            break

        bytes_read += len(chunk)
        chunks.append(chunk)

        if bytes_read > max_window_size:
            raise UnicodeError(
                f"Unable to decode frame after reading {bytes_read:,} bytes"
            )

        try:
            return b"".join(chunks).decode()
        except UnicodeDecodeError:
            continue

    return b"".join(chunks).decode()


def read_lines_zst(file_name):
    with open(file_name, "rb") as file_handle:
        buffer = ""
        reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(
            file_handle
        )
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)

            if not chunk:
                break
            lines = (buffer + chunk).split("\n")

            for line in lines[:-1]:
                yield line, file_handle.tell()

            buffer = lines[-1]

        reader.close()


def write_line_zst(handle, line):
    line_bytes = line.encode("utf-8")
    handle.write(line_bytes + b"\n")
