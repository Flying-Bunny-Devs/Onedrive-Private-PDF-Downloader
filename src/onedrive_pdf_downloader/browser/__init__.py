"""
Browser module for interacting with web browsers.
"""

from onedrive_pdf_downloader.browser.factory import (  # noqa: E501 pylint: disable=line-too-long
    browser_context,
    create_browser,
)
from onedrive_pdf_downloader.browser.utils import find_element, hide_toolbar

__all__ = ["create_browser", "browser_context", "find_element", "hide_toolbar"]
