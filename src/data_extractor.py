from RPA.Excel.Files import Files
from utils import resilient_action
import re
from requests import get
from uuid import uuid4
import os


class DataExtractor:
    """A class for extracting and storing data related to news articles.

    Methods:
    --------
    extract_data(search_result: dict) -> dict:
        Extracts relevant data from a given search result.

    store_data_to_excel(data: dict) -> None:
        Stores the extracted data into an Excel file.

        TODO
        Count of search phrases in the title and description
    """
    robot_root = os.environ.get('ROBOT_ROOT')
    excel_file_path = f"{robot_root}/devdata/scraped_data.xlsx"
    excel_file_name = "scraped_data.xlsx"
    headers = ["title", "money_pattern", "image", "date", "category"]

    def process_image(self, url):
        response = get(url)
        id = uuid4()
        file_path = f"{self.robot_root}/devdata/image_{id}.png"
        file_name = f"image_{id}.png"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download image, status code: {response.status_code}")
        # upload_file(file_path, file_name)
        return file_name

    def contains_money_patterns(self, input_str):
        patterns = [
            r"\$\d+\.\d{2}",  # $xx.x
            r"\$\d{1,3}(?:,\d{3})*\.\d{2}",  # $xxx,xxx.xx
            r"\d+ dollars",  # xx dollars
            r"\d+ USD",  # xx USD
        ]

        compound_pattern = "|".join(patterns)

        if re.search(compound_pattern, input_str):
            return True
        else:
            return False

    @resilient_action
    def extract_data(self, search_result):
        """Extract relevant data from a given search result.

        Parameters:
        -----------
        search_result : dict
            A dictionary containing the HTML elements or data of a search result.

        Returns:
        --------
        dict
            A dictionary containing the extracted data, such as title, date, and description.
        """
        extracted_data = {}
        try:
            title_element = search_result.get("title_element")
            time_element = search_result.get("time_element")
            category_element = search_result.get("category_element")
            image_element = search_result.get("image_element")

            if title_element:
                extracted_data["title"] = title_element.text
                extracted_data["money_pattern"] = self.contains_money_patterns(
                    extracted_data["title"]
                )
            if image_element:
                filename = self.process_image(image_element.get_attribute("src"))
                extracted_data["image"] = filename
            if time_element:
                extracted_data["date"] = time_element.get_attribute("datetime")
            if category_element:
                extracted_data["category"] = category_element.text
        except Exception as e:
            print(f"Failed to extract data: {e}")
        return extracted_data

    @resilient_action
    def store_data_to_excel(self, data):
        """Store the extracted data into an Excel file.

        Parameters:
        -----------
        data : dict
            A dictionarie of the extracted data.

        Returns:
        --------
        None
        """
        try:
            excel = Files()
            if os.path.exists(self.excel_file_path):
                excel.open_workbook(self.excel_file_path)
                excel.get_active_worksheet()
                excel.append_rows_to_worksheet([data])
            else:
                excel.create_workbook(self.excel_file_path)
                excel.get_active_worksheet()
                # fill headers
                col = 1
                for header in self.headers:
                    excel.set_cell_value(1, col, header)
                    col += 1

                # fill data
                col = 1
                for key in data:
                    excel.set_cell_value(2, col, data[key])
                    col += 1

            excel.save_workbook()
            excel.close_workbook()
            if not os.path.exists(self.excel_file_path):
                raise Exception("Excel file doesnt exists")

        except Exception as e:
            print(f"Failed to store data to Excel: {e}")
            raise Exception(e)
