"""Web scraper for extracting news data from Reuters.

This script leverages the Scraper and DataExtractor classes to execute web scraping.
The script performs the following tasks:

1. Retrieve work items for configuration settings
2. Open the Reuters website
3. Search for the specified term
4. Retrieve search results
5. Filter results by category and months
6. Extract relevant data from each result
7. Store extracted data in an Excel file
8. Upload the Excel file to Robocloud Artifacts
9. Write work items for output
10. Close the web browser

This script requires the 'RPA.Browser.Selenium', 'pandas', 'RPA.Robocorp.WorkItems',
and 'RPA.Robocloud.Items' packages.

TODO:
- Investigate if using assets is more efficient for uploading Excel and PNG files
"""

from scraper import Scraper
from data_extractor import DataExtractor
from RPA.Robocorp.WorkItems import WorkItems
import json
import logging.config


def setup_logging():
    with open("./logs/config.json", "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


setup_logging()
logger = logging.getLogger()


def main():
    """Execute the main workflow for web scraping from Reuters."""
    try:
        # Initialize and fetch work items
        library = WorkItems()
        library.get_input_work_item()
        inputs = library.get_work_item_variables()
        library.create_output_work_item()

        scraper = Scraper(inputs["settings"])
        extractor = DataExtractor(
            inputs["search_term"], inputs["category"], inputs["month_number"]
        )
        logger.info("Completed Step 1: Retrieved configurations and inputs.")

        # Open website
        scraper.open_website()
        logger.info(f"Completed Step 2: Opened {inputs['settings']['base_url']}.")

        # Perform search by term and category
        scraper.search_for_term_by_category(inputs["search_term"], inputs["category"])
        logger.info(
            f"Completed Steps 3 and 4: Searched for term '{inputs['search_term']}' under category '{inputs['category']}'."
        )

        # Initialize data container and loop through search results
        data = []
        scraped_iterations = 1
        while True:
            search_results = scraper.get_page_results()
            scraped_results = scraper.scrape_page(search_results)
            logger.info(
                f"Completed Step 5.{scraped_iterations}: Retrieved {len(search_results)} search results."
            )

            data_extracted = extractor.extract_from_page(scraped_results)
            if len(data_extracted) > 0:
                data.extend(data_extracted)

            if not scraper.go_to_next_page():
                break

            logger.info(f"Processed page {scraped_iterations}.")
            scraped_iterations += 1

        # Store data to Excel
        for item in data:
            extractor.store_data_to_excel(item)
        logger.info("Completed Steps 6 and 7: Extracted and stored data.")

        # Upload files
        library.add_work_item_file(extractor.excel_file_path)
        library.add_work_item_files("./data/*.png")
        logger.info("Completed Steps 8 and 9: Uploaded files.")

    except Exception as e:
        logger.critical(f"An unrecoverable error occurred: {e}")

    finally:
        # Cleanup
        scraper.close_browser()
        library.add_work_item_files("./logs/*.log")
        library.save_work_item()
        logger.info("Completed Step 10: Closed the web browser and saved logs.")


if __name__ == "__main__":
    main()
