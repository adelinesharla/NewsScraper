import pandas as pd
from .utils import resilient_action
import logging

# Configure logging to capture into a file
logging.basicConfig(level=logging.INFO, filename='../logs/data_extractor.log')
logger = logging.getLogger('DataExtractor')

class DataExtractor:
    """A class for extracting and storing data related to news articles.

    Methods:
    --------
    extract_data(search_result: dict) -> dict:
        Extracts relevant data from a given search result.

    store_data_to_excel(data: dict) -> None:
        Stores the extracted data into an Excel file.
    """

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
            # Supondo que 'title_element', 'date_element' e 'description_element'
            # sejam as chaves no dicionário search_result
            title_element = search_result.get('title_element')
            date_element = search_result.get('date_element')
            description_element = search_result.get('description_element')
            link_element = search_result.get('link_element')

            # Usando Selenium para extrair texto ou outros atributos dos elementos
            if title_element:
                extracted_data['title'] = title_element.text
            if link_element:
                extracted_data['link'] = link_element.get_attribute("href")
            if date_element:
                extracted_data['date'] = date_element.get_attribute("datetime")
            if description_element:
                extracted_data['description'] = description_element.text
        except Exception as e:
            logging.error(f"Failed to extract data: {e}")
        return extracted_data


    
    @resilient_action
    def store_data_to_excel(self, data):
        """Store the extracted data into an Excel file.

        Parameters:
        -----------
        data : list of dict
            A list containing dictionaries of the extracted data.

        Returns:
        --------
        None
        """
        try:
            # Criando um DataFrame a partir dos dados
            df = pd.DataFrame(data)

            # Definindo o nome do arquivo Excel
            excel_filename = "../data/scraped_data.xlsx"

            # Salvando o DataFrame em um arquivo Excel
            df.to_excel(excel_filename, index=False)

            logging.info(f"Data successfully saved to {excel_filename}")

        except Exception as e:
            logging.error(f"Failed to store data to Excel: {e}")
