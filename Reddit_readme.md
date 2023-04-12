# DataSIGNS
CMPT 733 - Term Project

## Subreddit Scraper

This is a Python script in the scripts/reddit folder that scrapes submissions from a given subreddit between two specified dates and outputs the data as a JSON file. It uses the Pushshift API to retrieve the data.

### Usage

To use the script, run subreddit_scraper.py with the following arguments:

`python redditApi.py --subreddit SUBREDDIT --start START_DATE --end END_DATE [--output OUTPUT_DIR] [--batch BATCH_SIZE] [--timeblock TIME_BLOCK]`

where:

*SUBREDDIT* is the name of the subreddit you want to scrape (default: "all") <br>
*START_DATE* is the start date for the search in "mm/dd/yyyy" format <br>
*END_DATE* is the end date for the search in "mm/dd/yyyy" format <br>
*OUTPUT_DIR* is the output directory for the scraped data (default: current directory) <br>
*BATCH_SIZE* is the number of submissions to retrieve per request (default: 1000) <br>
*TIME_BLOCK* is the time duration for each request in "hours:minutes" format (default: 1:0) <br>
The script will create a separate JSON file for each time block searched, with the filename formatted as {SUBREDDIT}_{START_DATE}to{END_DATE}.json. <br>

### Examples

To scrape all submissions from the "python" subreddit between January 1, 2022 and February 1, 2022 with a batch size of 500 and a time block of 2 hours, run the following command:

`python redditApi.py --subreddit python --start 01/01/2022 --end 02/01/2022 --batch 500 --timeblock 2:0`

The scraped data will be saved in the current directory as "python_01-01-2022to02-01-2022.json".
