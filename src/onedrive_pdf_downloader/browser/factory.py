"""
Factory module for creating browser instances.
"""

import argparse
import logging
import os
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def create_browser(args: argparse.Namespace) -> webdriver:
    """
    Create a browser instance based on the provided arguments.

    Args:
        args (argparse.Namespace): Command line arguments

    Returns:
        webdriver: The configured browser instance

    Raises:
        ValueError: If an unsupported browser is specified
    """
    options = None
    service = None

    logging.info("Initializing browser: '%s'", args.browser)

    match args.browser:
        case "firefox":
            options = webdriver.FirefoxOptions()
            service = FirefoxService(log_path=os.devnull)
            if args.profile_dir:
                options.profile = webdriver.FirefoxProfile(args.profile_dir)
            return webdriver.Firefox(service=service, options=options)

        case "chrome":
            options = webdriver.ChromeOptions()
            service = ChromeService(log_path=os.devnull)
            if args.profile_dir and args.profile_name:
                options.add_argument(f"user-data-dir={args.profile_dir}")
                options.add_argument(
                    f"--profile-directory={args.profile_name}")
            return webdriver.Chrome(service=service, options=options)

        case _:
            raise ValueError(f"Unsupported browser: {args.browser}")


@contextmanager
def browser_context(args: argparse.Namespace):
    """
    Context manager to handle the browser session.

    Args:
        args (argparse.Namespace): Command line arguments

    Yields:
        webdriver: The browser instance
    """
    browser = create_browser(args)
    try:
        yield browser
    finally:
        browser.quit()
        print()  # Add a new line after the browser is closed
        logging.info("Browser session ended.")
