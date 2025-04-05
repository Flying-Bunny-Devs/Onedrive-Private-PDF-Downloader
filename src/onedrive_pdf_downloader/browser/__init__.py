"""
Browser module for interacting with web browsers.
"""

from onedrive_pdf_downloader.browser.factory import create_browser, browser_context
from onedrive_pdf_downloader.browser.utils import find_element, hide_toolbar

__all__ = ["create_browser", "browser_context", "find_element", "hide_toolbar"]
