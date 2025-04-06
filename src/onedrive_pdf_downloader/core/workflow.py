"""
Main workflow for the PDF export process.
"""

import logging
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from onedrive_pdf_downloader.browser import browser_context, find_element
from onedrive_pdf_downloader.browser.constants import (
    CLASS_NAMES_FILE_NAME,
    CLASS_NAMES_TOTAL_PAGES,
)
from onedrive_pdf_downloader.core.export import export_pdf


def get_total_pages(browser) -> int:
    """
    Get the total number of pages from the page counter or manual input.

    Args:
        browser: Browser instance

    Returns:
        int: Total number of pages
    """
    try:
        total_text = find_element(
            browser, CLASS_NAMES_TOTAL_PAGES, By.CLASS_NAME).text
        total_of_pages = int(total_text.replace("/", ""))
        logging.info("Total number of pages detected: %d", total_of_pages)
    except (ValueError, NoSuchElementException):
        logging.warning(
            "The page counter is not visible or class names are not up-to-date."  # noqa: E501 pylint: disable=line-too-long
        )
        total_of_pages = int(
            input("Insert the total number of pages manually: "))

    return total_of_pages


def get_output_filename(args, browser) -> str:
    """
    Get the output filename from arguments, detected filename, or manual input.

    Args:
        args: Command line arguments
        browser: Browser instance

    Returns:
        str: Output filename
    """
    if args.output_file:
        return args.output_file

    try:
        filename = find_element(
            browser, CLASS_NAMES_FILE_NAME, By.CLASS_NAME).text
        logging.info("Detected file name: '%s'", filename)
        return filename
    except NoSuchElementException:
        logging.warning(
            "The file name is not visible or class names are not up-to-date."
        )
        filename = input(
            "Insert the file name manually (with the extension e.g.: file.pdf): "  # noqa: E501 pylint: disable=line-too-long
        )
        return filename


def export_pdf_workflow(args):
    """
    Execute the complete PDF export workflow.

    Args:
        args: Command line arguments

    Returns:
        bool: True if successful, False otherwise
    """
    with browser_context(args) as browser:
        browser.get(args.url)

        input(
            "Make sure to authenticate and reach the PDF preview. "
            "Once the file is loaded and the page counter is visible, press [ENTER] to start. "  # noqa: E501 pylint: disable=line-too-long
            "Keep the browser in the foreground for better results.\n> [ENTER] "  # noqa: E501 pylint: disable=line-too-long
        )
        sleep(2)  # Give a moment after user input before proceeding

        # Get number of pages and filename
        total_of_pages = get_total_pages(browser)
        filename = get_output_filename(args, browser)

        logging.info(
            'Starting the export of the file "%s". '
            "This might take a while depending on the number of pages.",
            filename
        )

        # Execute the PDF export
        return export_pdf(args, browser, total_of_pages, filename)
