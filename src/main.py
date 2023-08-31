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

This script requires the 'RPA.Browser.Selenium', 'pandas', 'RPA.Robocorp.WorkItems', 
and 'RPA.Robocloud.Items' libraries to be installed within the Python environment.
"""

from scraper import Scraper
from data_extractor import DataExtractor
from RPA.Robocorp.WorkItems import WorkItems
import os


def main():
    """Execute the main workflow for web scraping from Reuters."""
    library = WorkItems()
    library.get_input_work_item()
    config = library.get_work_item_variables()
    scraper = Scraper(config["settings"])
    extractor = DataExtractor()
    print("Step 1 done. Retrieved configs and inputs.")

    try:
        scraper.open_website()
        print(f"Step 2 done. Opened {config['settings']['base_url']} site")

        scraper.search_for_term(config["search_term"])
        print(f"Step 3 done. Searched for {config['search_term']}")

        search_results = scraper.get_search_results()
        print(f"Step 4 done. Retrieved the search results: {search_results}")

        for result in search_results:
            data = extractor.extract_data(result)
            extractor.store_data_to_excel(data)
        print("Step 5 and 6 done. Extracted and stored relevant data")
        files = WorkItems()
        files.add_work_item_file(extractor.excel_file_path)
        files.save_work_item()

        files.add_work_item_files("./data/*.png")
        files.save_work_item()
        print(
            f"Step 7 done. Uploaded the Excel and png files to Robocloud Artifacts: {extractor.excel_file_path}"
        )

        output_work_item_data = {
            "status": "completed",
            "excel_file": extractor.excel_file_name,
        }

        library.create_output_work_item(output_work_item_data)
        library.save_work_item()
        print("Step 8 done. Wrote work items for output")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        scraper.close_browser()
        print("Step 9 done. Closed the web browser")


if __name__ == "__main__":
    main()
