import re
from typing import Dict


def find_match(line: str, patterns: Dict[str, re.Pattern]) -> (Dict[str, str], str):
    """ Finds the first matching pattern for the input line. Returns the groups matching and the name of the matching format. """

    for format_name, pattern in patterns.items():
        match = pattern.match(line)

        if match:
            groups = match.groupdict()
            return groups, format_name

    return None, None