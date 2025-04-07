"""
Utility functions for browser interaction.
"""

import logging

from selenium import webdriver
from selenium.common.exceptions import (  # noqa: E501 pylint: disable=line-too-long
    JavascriptException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By

from onedrive_pdf_downloader.browser.constants import CLASS_NAMES_TOOLBAR


def find_element(browser: webdriver, identifiers: list[str], by: By):
    """
    Find an element using multiple possible identifiers.

    Args:
        browser (webdriver): Browser instance
        identifiers (list[str]): List of identifiers to try
        by (By): The method to use for finding the element

    Returns:
        WebElement: The found element

    Raises:
        NoSuchElementException: If no element is found with any identifier
    """
    for identifier in identifiers:
        try:
            match by:
                case By.CLASS_NAME:
                    element = browser.find_element(by, identifier)
                case By.XPATH:
                    element = browser.find_elements(
                        by, f"//button[@aria-label='{identifier}']"
                    )[-1]
                case _:
                    raise ValueError(f"Unsupported method: {by}")
            logging.debug("Element found using %s: '%s'", by, identifier)
            return element
        except (NoSuchElementException, IndexError):
            logging.debug("Element not found using %s: '%s'", by, identifier)
            continue

    raise NoSuchElementException(
        f"No element found with any of the identifiers: {identifiers}"
    )


def hide_toolbar(browser: webdriver, class_names: list[str] = None) -> None:
    """
    Hide the toolbar to get clean screenshots.

    Args:
        browser (webdriver): Browser instance
        class_names (list[str]): List of possible class names for the toolbar

    Raises:
        NoSuchElementException: If no toolbar is found
    """

    if class_names is None:
        class_names = CLASS_NAMES_TOOLBAR
    for class_name in class_names:
        try:
            browser.execute_script(
                f"document.getElementsByClassName('{class_name}')[0].style.visibility = 'hidden'"  # noqa: E501 pylint: disable=line-too-long
            )
            logging.debug("Toolbar hidden using class name: '%s'", class_name)
            return
        except (IndexError, NoSuchElementException, JavascriptException):
            logging.debug(
                "Toolbar not found using class name: '%s'", class_name
            )
            continue

    raise NoSuchElementException(
        f"No toolbar found with any of the class names: {class_names}"
    )
