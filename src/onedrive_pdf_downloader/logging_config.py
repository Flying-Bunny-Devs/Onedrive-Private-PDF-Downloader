"""
Logging configuration for the application.
"""

import logging


def setup_logging(debug_mode: bool = False) -> None:
    """
    Set up logging configuration.

    Args:
        debug_mode: Whether to enable debug logging
    """
    log_level = logging.DEBUG if debug_mode else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s - %(message)s",
    )

    # Silence noisy libraries unless in debug mode
    if not debug_mode:
        logging.getLogger("img2pdf").setLevel(logging.ERROR)
        logging.getLogger("selenium").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("PIL").setLevel(logging.ERROR)
