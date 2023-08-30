import json
import functools
from RPA.Robocloud.Items import Items
import requests
from requests import get
from uuid import uuid4

def process_image(url):
    response = get(url)
    id = uuid4()
    file_path = f"./data/image_{id}.png"
    file_name = "image_{id}.png"
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download image, status code: {response.status_code}")
    #upload_file(file_path, file_name)
    return file_name


def upload_file(file_path, file_name):
    items = Items()
    items.add_file(file_path, name=file_name)


def read_config(file_path):
    """Read JSON configuration from a file and return as a dictionary.

    Parameters:
        file_path (str): The path to the configuration file.

    Returns:
        dict: The JSON content parsed into a dictionary.
    """
    with open(file_path, "r") as f:
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
