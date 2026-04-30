from typing import Optional
import re
import logging

from datas import LineParts

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

