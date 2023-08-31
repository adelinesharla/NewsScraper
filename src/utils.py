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


def resilient_action(retries=3, delay=5):
    """Decorator to add resilience to a function by catching exceptions.

    This decorator catches any exceptions that occur when executing the wrapped function.
    Additional resilience logic retries added.

    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function with added resilience.
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
                    # If an exception other than the ones listed occurs, raise it and terminate the script.
                    print(f"An unrecoverable error occurred: {e}")
                    logger.error(
                        f"An unrecoverable error occurred while executing {func.__name__}: {e}"
                    )
                    raise e  # Raising the exception will terminate the script

        return wrapper
