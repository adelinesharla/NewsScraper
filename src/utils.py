import json
import functools
from selenium.webdriver.common.by import By

def read_config(file_path):
    """Read JSON configuration from a file and return as a dictionary.
    
    Parameters:
        file_path (str): The path to the configuration file.
    
    Returns:
        dict: The JSON content parsed into a dictionary.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def resilient_action(func):
    """Decorator to add resilience to a function by catching exceptions.
    
    The decorated function will catch any exceptions and print an error message.
    Additional resilience logic like retrying or logging can be added.
    
    Parameters:
        func (callable): The function to be wrapped.
        
    Returns:
        callable: The wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Add retry logic or logging here
    return wrapper

def find_child_element(parent_element, css_selector):
    try:
        return parent_element.find_element(By.CSS_SELECTOR, css_selector)
    except:
        return None