import json
import functools
import logging

# Configure logging to capture errors and other events
logging.basicConfig(level=logging.ERROR, filename="./logs/errors.log")
logger = logging.getLogger("ResilientDecorator")

def resilient_action(func):
    """Decorator to add resilience to a function by catching exceptions.

    This decorator catches any exceptions that occur when executing the wrapped function.
    It prints an error message and logs it. Additional resilience logic like retries can be added.

    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function with added resilience.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"An error occurred while executing {func.__name__}: {e}")
            # Uncomment the following line to add retry logic if needed
            # return retry_logic(*args, **kwargs)

    return wrapper

# Uncomment the following lines to add a retry logic function if needed
# def retry_logic(*args, **kwargs):
#     # Implement retry logic here
#     pass
