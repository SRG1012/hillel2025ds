import time
import logging
from copy import deepcopy

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# =============================================================
# TimerContext: A context manager to measure execution time
# =============================================================
class TimerContext:
    def __enter__(self):
        self.start_time = time.time()  # Record the start time
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()  # Record the end time
        elapsed_time = self.end_time - self.start_time
        logging.info(f"Execution time: {elapsed_time:.4f} seconds")

# Test TimerContext
with TimerContext():
    time.sleep(2)  # Simulate some work

# =============================================================
# Configuration: A context manager to manage temporary global configuration
# =============================================================
GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}

class Configuration:
    def __init__(self, updates, validator=None):
        """Context manager for temporarily modifying the global configuration."""
        self.updates = updates
        self.validator = validator
        self.original_config = None

    def __enter__(self):
        """Apply updates to the global configuration."""
        global GLOBAL_CONFIG
        self.original_config = deepcopy(GLOBAL_CONFIG)  # Save the original config
        GLOBAL_CONFIG.update(self.updates)  # Apply updates
        logging.info(f"Applied updates: {self.updates}")

        # If a validator is provided, validate the configuration immediately
        if self.validator and not self.validator(GLOBAL_CONFIG):
            logging.error("Validation failed during __enter__. Reverting changes.")
            GLOBAL_CONFIG = self.original_config
            raise ValueError("Invalid configuration")

    def __exit__(self, exc_type, exc_value, traceback):
        """Restore the original configuration."""
        global GLOBAL_CONFIG
        if exc_type:
            logging.error(f"Exception occurred: {exc_value}. Reverting to original config.")
        else:
            # Optionally validate the configuration before exiting
            if self.validator and not self.validator(GLOBAL_CONFIG):
                logging.error("Validation failed during __exit__. Reverting changes.")

        # Always restore the original configuration
        GLOBAL_CONFIG = self.original_config
        logging.info("Configuration restored to original state.")

# Example validator function

def validate_config(config: dict) -> bool:
    """Ensure 'max_retries' is non-negative."""
    if config.get("max_retries", 0) < 0:
        logging.error("Validation failed: 'max_retries' must be non-negative.")
        return False
    return True

# Test Configuration context manager
if __name__ == "__main__":
    logging.info("Initial GLOBAL_CONFIG: %s", GLOBAL_CONFIG)

    # Example 1: Successful configuration update
    try:
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info("Inside context (valid): %s", GLOBAL_CONFIG)
    except Exception as e:
        logging.error("Error: %s", e)

    logging.info("After context (valid): %s", GLOBAL_CONFIG)

    # Example 2: Configuration update with validation failure
    try:
        with Configuration({"feature_a": "invalid_value", "max_retries": -1}, validator=validate_config):
            logging.info("Inside context (invalid): %s", GLOBAL_CONFIG)
    except Exception as e:
        logging.error("Caught exception: %s", e)

    logging.info("After context (invalid): %s", GLOBAL_CONFIG)
