"""
Command line interface configuration for the application.
"""

import argparse

from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command line argument parser.

    Returns:
        argparse.ArgumentParser: The configured parser
    """
    parser = argparse.ArgumentParser(
        description="Export a PDF (also the protected ones) from an authenticated session.",  # noqa: E501 pylint: disable=line-too-long
        epilog="Made with ❤️ by @Francesco146 and @willnaoosmith",
    )

    # Version option
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version of the script",
    )

    # Browser options
    parser.add_argument(
        "--browser", "-b",
        type=str,
        choices=["firefox", "chrome"],
        help="Browser to use (firefox or chrome)",
        default="firefox",
        metavar="BROWSER",
    )
    parser.add_argument(
        "--profile-dir", "-p",
        type=str,
        help="Path to the browser profile.",
        default=None,
        metavar="PATH",
    )
    parser.add_argument(
        "--profile-name", "-n",
        type=str,
        help="Profile name to use, only for Chrome.",
        default=None,
        metavar="PATH",
    )

    # Output options
    parser.add_argument(
        "--output-file", "-o",
        type=str,
        help="Specify the output file name",
        required=False,
        metavar="FILE",
    )
    parser.add_argument(
        "--keep-imgs", "-k",
        action="store_true",
        help="Keep the images after the PDF creation",
        default=False,
    )

    # Cache options
    parser.add_argument(
        "--cache-dir", "-r",
        help=(
            "Search in browser caches for RAW Lossless PDFs, only works with Firefox. "  # noqa: E501 pylint: disable=line-too-long
            "\033[93m\033[1mWARNING: Highly experimental, may cause problems. "
            "Read the documentation before using.\033[0m"
        ),
        required=False,
        metavar="PATH",
    )

    # Debug options
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Show debug messages",
        default=False,
    )

    # URL argument
    parser.add_argument(
        "url",
        type=str,
        help="URL of the PDF file"
    )

    return parser
