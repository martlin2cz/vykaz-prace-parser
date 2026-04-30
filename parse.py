from typing import List, Optional
import re
import logging

import pathlib

from datas import LineParts

########################################################################################################################


class FileParser:
    """ The file parser. Parses the file into lines, and then parses each line into its parts. """

    @staticmethod
    def parse_file(path: pathlib.Path) -> List[LineParts]:
        """
        Parses the file content into a list of LineParts.
        """

        lines = FileParser._load_lines_(path)

        records: List[LineParts] = []

        for line in lines:

            parts = LineParser.detect_parts(line)
            if parts:
                records.append(parts)
                logging.info("%s OK", parts.date_part)

        return records

    @staticmethod
    def _load_lines_(path: pathlib.Path) -> List[str]:
        """
        Loads all non-empty lines from a text file using US-ASCII encoding.
        """
        with open(path, "r", encoding="ascii") as fh:
            return [line.strip() for line in fh if line.strip()]

########################################################################################################################


class LineParser:
    """ The line parser. Parses the line into its parts: date, task list, and hours list. """

    @staticmethod
    def detect_parts(line: str) -> Optional[LineParts]:
        """
        Detects date, task list, and hours list sections from an input line.
        """
        pattern = re.compile(
            r"^(?P<date>\d{2}\.\d{2}\.\d{4})\s+-\s+"
            r"(?P<tasks>.+?)\s*"
            r"\((?P<hours>[^)]+)\)$"
        )

        match = pattern.match(line)

        if not match:
            logging.error("Failed to detect parts: %s", line)
            return None

        return LineParts(
            date_part=match.group("date"),
            task_list_part=match.group("tasks"),
            hours_list_part=match.group("hours"),
        )


########################################################################################################################

