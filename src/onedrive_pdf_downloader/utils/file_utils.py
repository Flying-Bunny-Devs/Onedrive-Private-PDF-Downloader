"""
File-related utility functions.
"""

import argparse
import logging
import shutil
import time

from onedrive_pdf_downloader.cache.finder import find_pdf_in_cache


def get_default_filename() -> str:
    """
    Generate a default filename based on current timestamp.

    Returns:
        str: Default filename with timestamp
    """
    return f"{time.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"


def copy_cached_pdf(args: argparse.Namespace) -> bool:
    """
    Copy a PDF file from browser cache if available.

    Args:
        args: Command line arguments

    Returns:
        bool: True if successfully copied, False otherwise
    """
    try:
        pdf_file = find_pdf_in_cache(args.cache_dir)
        logging.debug("Found PDF file in the cache: '%s'", pdf_file)

        filename = args.output_file or get_default_filename()

        if not args.output_file:
            logging.warning(
                "Output file name not specified. Using the current timestamp."
            )

        shutil.copy(pdf_file, filename)
        logging.info("PDF file copied to '%s'", filename)
        return True

    except FileNotFoundError:
        logging.error(
            "No PDF file found in the cache directory, continuing with browser-based export."  # noqa: E501 pylint: disable=line-too-long
        )
        return False
    except IOError as e:
        logging.error("Error copying cached PDF: %s", str(e))
        return False
