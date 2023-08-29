"""Web scraper for extracting news data from Reuters.

This script uses the Scraper and DataExtractor classes to perform web scraping.
The script performs the following tasks:

1. Reads work items for configuration settings
2. Opens the Reuters website
3. Searches for a term ("climate change" in this example)
4. Retrieves the search results
5. Extracts relevant data from each result
6. Stores the extracted data in an Excel file
7. Writes work items for output
8. Closes the web browser

This script requires that the 'RPA.Browser.Selenium', 'pandas', and 'RPA.Robocorp.WorkItems' libraries are installed within the Python environment.
"""

from scraper import Scraper
from data_extractor import DataExtractor
from RPA.Robocorp.WorkItems import WorkItems
from utils import read_config

def main():
    """Execute the main workflow for web scraping from Reuters.

    Steps:
    1. Load configuration settings from work items.
    2. Initialize scraper and data extractor classes.
    3. Open the Reuters website.
    4. Search for a given term.
    5. Scrape and extract data for each search result.
    6. Store the extracted data in an Excel file.
    7. Write output to work items.
    8. Close the web browser.
    """

    work_items = WorkItems()
    input_work_item = work_items.load_work_item()
    config = input_work_item["config"]

    scraper = Scraper(config)
    extractor = DataExtractor()

    try:
        scraper.open_website()
        scraper.search_for_term(config.get("search_term", "climate change"))
        search_results = scraper.get_search_results()

        for result in search_results:
            data = extractor.extract_data(result)
            extractor.store_data_to_excel(data)

        output_work_item = {
            "status": "completed",
            "excel_file": extractor.excel_file_path
        }
        
        work_items.save_work_item(output_work_item)

    finally:
        scraper.close_browser()

if __name__ == "__main__":
    main()
