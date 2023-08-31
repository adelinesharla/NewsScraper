import functools
import logging
import time
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    UnexpectedAlertPresentException,
    SessionNotCreatedException,
    InvalidSessionIdException,
)

# Configure logging to capture errors and other events
logging.basicConfig(level=logging.ERROR, filename="./logs/errors.log")
logger = logging.getLogger("ResilientDecorator")

class MaxRetriesReachedError(Exception):
    """Exception raised when the maximum number of retries is reached."""
    pass

def resilient_action(_func=None, *, retries=3, delay=5):
    """Decorator to add resilience to a function by catching exceptions.

    Args:
        retries (int, optional): Number of retry attempts. Default is 3.
        delay (int, optional): Delay in seconds between retries. Default is 5.

    Returns:
        callable: The wrapped function with added resilience.

    TODO:
        - Understand which parameters use in functions, testing and analising
        - Check for more exceptions that could be retried
        - Check actions to do before retry (for exemplo in open website should close all others first)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except (
                    TimeoutException,
                    NoSuchElementException,
                    StaleElementReferenceException,
                    WebDriverException,
                    ElementClickInterceptedException,
                    ElementNotInteractableException,
                    UnexpectedAlertPresentException,
                    SessionNotCreatedException,
                    InvalidSessionIdException,
                ) as e:
                    print(f"A retryable error occurred: {e}")
                    logger.error(
                        f"A retryable error occurred while executing {func.__name__}: {e}"
                    )

                    if attempt < retries:
                        print(
                            f"Retrying in {delay} seconds... (Attempt {attempt}/{retries})"
                        )
                        time.sleep(delay)
                    else:
                        print(f"Failed after {retries} attempts.")
                        raise MaxRetriesReachedError(
                            f"Failed after {retries} attempts."
                        )
                except Exception as e:
                    print(f"An unrecoverable error occurred: {e}")
                    logger.error(
                        f"An unrecoverable error occurred while executing {func.__name__}: {e}"
                    )
                    raise e
        return wrapper
    
    if _func is None:
        return decorator
    else:
        return decorator(_func)

