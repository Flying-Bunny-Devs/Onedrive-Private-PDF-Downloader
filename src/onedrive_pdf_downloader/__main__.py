#!/usr/bin/env python3
"""
Entry point for the OneDrive PDF Downloader application.
"""

import argparse
import logging
import sys

from onedrive_pdf_downloader.cli import create_parser
from onedrive_pdf_downloader.core import export_pdf_workflow
from onedrive_pdf_downloader.cache import find_pdf_in_cache
from onedrive_pdf_downloader.logging_config import setup_logging


def main() -> None:
    """Main function to execute the PDF export workflow."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging based on debug flag
    setup_logging(debug_mode=args.debug)

    try:
        # Try to find PDF in cache if requested
        if args.cache_dir and args.browser == "firefox":
            from onedrive_pdf_downloader.utils import copy_cached_pdf
            if copy_cached_pdf(args):
                return

        # If cache not found or not requested, proceed with browser-based workflow
        export_pdf_workflow(args)

    except Exception as e:
        logging.error("Error during execution: %s", str(e))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
