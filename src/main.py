"""Web scraper for extracting news data from Reuters.

This script uses the Scraper and DataExtractor classes to perform web scraping.
The script performs the following tasks:

1. Reads the configuration settings
2. Opens the Reuters website
3. Searches for a term ("climate change" in this example)
4. Retrieves the search results
5. Extracts relevant data from each result
6. Stores the extracted data in an Excel file
7. Closes the web browser

This script requires that the 'RPA.Browser.Selenium' and 'pandas' libraries are installed within the Python environment.
"""

from scraper import Scraper
from data_extractor import DataExtractor
from utils import read_config


def main():
    """Execute the main workflow for web scraping from Reuters.

    Steps:
    1. Load configuration settings.
    2. Initialize scraper and data extractor classes.
    3. Open the Reuters website.
    4. Search for a given term.
    5. Scrape and extract data for each search result.
    6. Store the extracted data in an Excel file.
    7. Close the web browser.
    """

    config = read_config("../config/settings.json")
    scraper = Scraper(config)
    extractor = DataExtractor()

    try:
        scraper.open_website()
        scraper.search_for_term("climate change")
        search_results = scraper.get_search_results()

        for result in search_results:
            data = extractor.extract_data(result)
            extractor.store_data_to_excel(data)
    finally:
        scraper.close_browser()


if __name__ == "__main__":
    main()
