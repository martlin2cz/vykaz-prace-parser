import logging
import argparse
from pathlib import Path

from parse import RecordsParser

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def _create_parser_() -> argparse.ArgumentParser:
    """
    Creates and returns the argument parser for the application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "INFILE",
        type=Path,
        help="Input text file containing task records",
    )
    return parser


def _main_() -> None:
    """
    Application entry point.
    """
    parser = _create_parser_()
    args = parser.parse_args()

    if not args.INFILE.is_file():
        raise FileNotFoundError(str(args.INFILE))

    parser = RecordsParser()
    parser.process_file(args.INFILE)


if __name__ == "__main__":
    _main_()
