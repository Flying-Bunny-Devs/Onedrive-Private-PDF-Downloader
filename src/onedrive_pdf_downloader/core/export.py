"""
Core functionality for exporting PDFs from web browser.
"""

import logging
import os
import shutil
import tempfile
from time import sleep

import img2pdf
from selenium.common.exceptions import (  # noqa: E501 pylint: disable=line-too-long
    JavascriptException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By

from onedrive_pdf_downloader.browser.constants import ARIA_LABELS_NEXT_PAGE
from onedrive_pdf_downloader.browser.utils import find_element, hide_toolbar


def export_pdf(args, browser, total_of_pages, filename):
    """
    Export the PDF by taking screenshots of each page.

    Args:
        args (argparse.Namespace): Command line arguments
        browser (webdriver): Browser instance
        total_of_pages (int): Total number of pages
        filename (str): Output filename

    Returns:
        bool: True if successful, False otherwise
    """
    files_list = []

    with tempfile.TemporaryDirectory() as temp_dir:
        # Hide the toolbar for screenshots
        try:
            hide_toolbar(browser)
            logging.info("Toolbar hidden for clean screenshots.")
        except NoSuchElementException:
            logging.warning(
                "The toolbar is not visible or class names are not up-to-date. "  # noqa: E501 pylint: disable=line-too-long
                "Screenshots might contain the toolbar."
            )

        # Process each page
        page_number = 1
        while page_number <= total_of_pages:
            sleep(5)  # Wait for page to load properly
            image_path = f"{temp_dir}/{str(page_number)}.png"

            try:
                browser.find_element(
                    By.CSS_SELECTOR, "canvas").screenshot(image_path)
            except NoSuchElementException:
                logging.error(
                    "Cannot find the PDF canvas within the page. "
                    "This may be due to internal changes in OneDrive."
                )
                return False

            files_list.append(image_path)

            logging.info(
                "Page %s of %s exported.",
                str(page_number),
                str(total_of_pages)
            )

            page_number += 1

            # Go to the next page if not on the last page
            if page_number <= total_of_pages:
                try:
                    next_page_button = find_element(
                        browser, ARIA_LABELS_NEXT_PAGE, By.XPATH
                    )
                    browser.execute_script(
                        "arguments[0].click();", next_page_button)
                except (NoSuchElementException, JavascriptException):
                    logging.error(
                        "Cannot find the next page button. Navigation aria labels may be outdated. "  # noqa: E501 pylint: disable=line-too-long
                        "Saving the pages obtained so far."
                    )
                    break

        # Save the PDF
        try:
            logging.info("Saving the file as '%s'.", filename)
            with open(filename, "wb") as out_file:
                out_file.write(img2pdf.convert(files_list))

            # Save images if requested
            if args.keep_imgs:
                keep_dir = f"{filename}_images"
                os.makedirs(keep_dir, exist_ok=True)
                for file_path in files_list:
                    shutil.copy(file_path, keep_dir)
                logging.info("Images kept in directory '%s'.", keep_dir)

            logging.info("PDF export completed successfully.")
            return True

        except IOError as e:
            logging.error("Error saving PDF: %s", str(e))
            return False
