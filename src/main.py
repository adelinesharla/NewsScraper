"""Web scraper for extracting news data from Reuters.

This script uses the Scraper and DataExtractor classes to perform web scraping.
The script performs the following tasks:

1. Reads work items for configuration settings
2. Opens the Reuters website
3. Searches for a term ("climate change" in this example)
4. Retrieves the search results
5. Extracts relevant data from each result
6. Stores the extracted data in an Excel file
7. Uploads the Excel file to Robocloud Artifacts
8. Writes work items for output
9. Closes the web browser

This script requires that the 'RPA.Browser.Selenium', 'pandas', 'RPA.Robocorp.WorkItems', and 'RPA.Robocloud.Items' libraries are installed within the Python environment.
"""

from scraper import Scraper
from data_extractor import DataExtractor
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Robocloud.Items import Items
from utils import configure_logging

logger = configure_logging("Scraper", "../logs/scraper.log")


def main():
    """Execute the main workflow for web scraping from Reuters.

        Steps:
    1. Reads work items for configuration settings
    2. Opens the Reuters website
    3. Searches for a term ("climate change" in this example)
    4. Retrieves the search results
    5. Extracts relevant data from each result
    6. Stores the extracted data in an Excel file
    7. Uploads the Excel file to Robocloud Artifacts
    8. Writes work items for output
    9. Closes the web browser
    """

    work_items = WorkItems()
    input_work_item = work_items.load_work_item()
    config = input_work_item["config"]

    scraper = Scraper(config)
    extractor = DataExtractor()

    try:
        scraper.open_website()
        scraper.search_for_term(config.get("search_term"))
        search_results = scraper.get_search_results()

        for result in search_results:
            data = extractor.extract_data(result)
            extractor.store_data_to_excel(data)

        # Upload the Excel file to Robocloud Artifacts
        items = Items()
        items.init()

        # Fazendo o upload para Robocloud Artifacts
        items.add_file(extractor.excel_file_path, name=extractor.excel_file_path)

        output_work_item = {
            "status": "completed",
            "excel_file": extractor.excel_file_path,
        }

        work_items.save_work_item(output_work_item)

    finally:
        scraper.close_browser()


if __name__ == "__main__":
    main()
