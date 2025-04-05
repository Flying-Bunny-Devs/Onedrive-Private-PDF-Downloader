"""
Functions for finding PDF files in browser cache.
"""

import logging
import os


def find_pdf_in_cache(cache_dir: str) -> str:
    """
    Find the most recent PDF file in the browser cache directory.

    Identifies PDF files by reading the first 4 bytes of each file.

    Args:
        cache_dir (str): Path to the browser cache directory

    Returns:
        str: Path to the most recent PDF file

    Raises:
        FileNotFoundError: If no PDF file is found in the cache directory
    """
    pdf_files = []

    for root, _, files in os.walk(cache_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    first_4_bytes = f.read(4)
                    if first_4_bytes == b'%PDF':
                        pdf_files.append(file_path)
                        logging.debug("Found PDF file: %s", file_path)
            except (IOError, PermissionError) as e:
                logging.debug("Could not read file %s: %s", file_path, str(e))
                continue

    if not pdf_files:
        raise FileNotFoundError("No PDF file found in the cache directory.")

    # Return the most recently modified PDF file
    most_recent = max(pdf_files, key=os.path.getmtime)
    logging.debug("Most recent PDF file: %s", most_recent)
    return most_recent
