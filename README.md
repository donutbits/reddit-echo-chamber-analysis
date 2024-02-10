# Subreddit Echo Chamber Analysis

## Description

This repo contains Jupyter notebooks and Python scripts for an analysis of echo chambers in political subreddits. The analysis examines submissions and comments from 7 subreddits over a 4-year period.

## Contents

- `data/`: Raw subreddit data as CSVs
- `data_cleaning/`
    - `0 - API Test.ipynb`: Early work for using Reddit's API to access the data.
    - `1 - Subset Data.ipynb`: First step in data cleaning was to select only the fields required to reduce data volume.
    - `2 - Data Cleaning.ipynb`: Steps to clean text from comments and submissions
- `analysis/`
  - `3 - Exploratory Analysis.ipynb`: Exploratory data analysis on word frequencies, word clouds
  - `4 - Topic Moswlinf.ipynb`: Topic modeling with LDA
  - `5 - Sentiment Analysis.ipynb`: Sentiment analysis on comments
- `future_work/`
  - `6 - Network Analysis.ipynb`: Future work for analyzing network effects in comments
- `pyproject.toml`: Required Python packages

## Usage

1. Clone this repo
2. Install poetry: `pip install poetry`
3. Install environment: `poetry install`  
4. Activate environment: `poetry shell`
5. Run Jupyter notebooks

## Data

Early in the process, the data was being obtained directly from the Reddit API.
Unfortunately, Reddit changed access in the middle of the analysis and this approach was discarded.
Instead, data was obtained from https://the-eye.eu/redarcs/ by downloading the
submissions and comments of the following subreddits:
- Conservative
- Progressive
- Democrats
- Republican
- NeutralPolitics
- PoliticalDiscussion
- Politics

## Results

- Subreddits categorized into left-leaning, right-leaning, and neutral groups based on language use
- Topic models show distinct topics discussed in each subreddit
- Sentiment analysis reveals different emotional tones by subreddit

