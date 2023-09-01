import functools
import logging
import time
import traceback
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
import logging

logger = logging.getLogger(__name__)



class MaxRetriesReachedError(Exception):
    """Exception raised when the maximum number of retries is reached."""

    pass


def resilient_action(_func=None, *, retries=3, delay=10):
    """Decorator to add resilience to a function by catching exceptions.

    Args:
        retries (int, optional): Number of retry attempts. Default is 3.
        delay (int, optional): Delay in seconds between retries. Default is 5.

    Returns:
        callable: The wrapped function with added resilience.

    TODO:
        - Understand which parameters use in functions, testing and analising
        - Check for more exceptions that could be retried
        - Check actions to do before retry (for example in open website should close all others first)
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
                    tb = traceback.extract_tb(e.__traceback__)
                    last_trace = tb[-1] if tb else None
                    line = last_trace[1] if last_trace else "Unknown"
                    logger.error(
                        f"A retryable error occurred while executing {func.__name__} at line {line}: {e} {e.__class__.__name__}"
                    )

                    if attempt < retries:
                        logger.warning(
                            f"Retrying in {delay} seconds... (Attempt {attempt}/{retries})"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"Failed after {retries} attempts.")
                        raise MaxRetriesReachedError(
                            f"Failed after {retries} attempts."
                        )
                except Exception as e:
                    tb = traceback.extract_tb(e.__traceback__)
                    last_trace = tb[-1] if tb else None
                    line = last_trace[1] if last_trace else "Unknown"
                    logger.error(
                        f"An unrecoverable error occurred while executing {func.__name__} at line {line}: {e} {e.__class__.__name__}"
                    )
                    raise e

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
