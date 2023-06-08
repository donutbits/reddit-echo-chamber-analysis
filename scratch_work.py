# Scratch work
SELECT subreddit, COUNT(*) AS comments_count
FROM `fh-bigquery.reddit_comments.20*`
WHERE subreddit IN ("politics", "Conservative", "Republican", "socialism", "democrats", "NeutralPolitics", "Libertarian", "PoliticalHumor")
GROUP BY subreddit
ORDER BY 2 DESC;

# https://www.reddit.com/r/bigquery/comments/3cej2b/17_billion_reddit_comments_loaded_on_bigquery/


# Get recent data from specific subreddits
# https://www.reddit.com/r/pushshift/comments/13oxo45/retrieve_comments_in_a_subreddit_using_python/

# List of subreddits to pull comments from
political_subreddits = {'NeutralPolitics': {'partisanship': 'Neutral', 'subscribers': 612392},
                        'PoliticalCompassMemes': {'partisanship': 'Neutral', 'subscribers': 574582},
                        'PoliticalHumor': {'partisanship': 'Neutral', 'subscribers': 1582739},
                        'politics': {'partisanship': 'Neutral', 'subscribers': 8328845},
                        'PoliticalDiscussion': {'partisanship': 'Neutral', 'subscribers': 2179609},
                        'moderatepolitics': {'partisanship': 'Neutral', 'subscribers': 287029},
                        'Libertarian': {'partisanship': 'Right-Leaning', 'subscribers': 511965},
                        'Republican': {'partisanship': 'Right-Leaning', 'subscribers': 0},
                        'Conservative': {'partisanship': 'Right-Leaning', 'subscribers': 1038900},
                        'gunpolitics': {'partisanship': 'Right-Leaning', 'subscribers': 124901},
                        'Socialism': {'partisanship': 'Left-Leaning', 'subscribers': 0},
                        'democrats': {'partisanship': 'Left-Leaning', 'subscribers': 0},
                        'latestagecapitalism': {'partisanship': 'Left-Leaning', 'subscribers': 0}}