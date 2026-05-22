import dataclasses
import re
import typing
from collections import OrderedDict
from abc import abstractmethod, ABC
from typing import Dict, List, Tuple, TypeVar
from datas import DetectedErrors
from lexer import AbstractTokeniser, AbstractCharacterClassifier, SimpleLexer


def find_match(line: str, patterns: Dict[str, re.Pattern]) -> (Dict[str, str], str):
    """ Finds the first matching pattern for the input line. Returns the groups matching and the name of the matching format. """

    for format_name, pattern in patterns.items():
        match = pattern.match(line)

        if match:
            groups = match.groupdict()
            return groups, format_name

    return None, None


def find_match_range(text: str, patterns: Dict[str, re.Pattern]) -> (Tuple[int, int], str):
    """ Finds the first matching pattern for the text. Returns the range with start and end indexes """

    for format_name, pattern in patterns.items():
        match = pattern.search(text)

        if match:
            span = match.span()
            return (span[0], span[1]), format_name

    return None, None


class SplitBacketedByCommaCharacterClassifier(AbstractCharacterClassifier):
    """ The character classifier which detects the backetted text, normal (unbracketed text), comma as delimiter and space(s). """

    def __init__(self):
        self.brackets_level = 0

    def class_of_char(self, i: int, char: str, text: str) -> str:
        if char == "(":
            self.brackets_level += 1
            return "B"

        if char == ")":
            self.brackets_level -= 1
            return "B"

        if self.brackets_level > 0:
            return "B"

        if char == ",":
            return "D"

        if char.isspace():
            return "S"

        return "T"


class SplitBacketedByCommaTokeniser(AbstractTokeniser):
    """ The tokeniser which detects the taskswith bracketed description, separated by comma, allowing either of them to be ommited. """

    def __init__(self, errors: DetectedErrors):
        self.patterns = OrderedDict([
            ("format:standart delim:standart", re.compile("^(T[TS]*)(B+S*)(DS*|$)")),
            ("format:simple delim:standart",   re.compile("^(T[TS]*)(DS*|$)")),
            ("format:missing-id delim:standart", re.compile("^(B+S*)(DS*|$)")),

            ("format:standart delim:not", re.compile("^(T[TS]*)(B+S*)(?!D|$)")),
            ("format:simple delim:not",   re.compile("^T[TS]*(?!D|$)")),
            ("format:missing-id delim:not",   re.compile("^(B+S*)(?!D|$)")),
        ])
        self.errors = errors

    def find_matching_token(self, char_classes_substr: str, chars_subst: str) -> re.Match | typing.Tuple[int, int] | None:
        _range, pattern_name = find_match_range(char_classes_substr, self.patterns)

        if "format:missing-id" in pattern_name:
            self.errors.add_minor(f"Invalid task format: {chars_subst[_range[0]:_range[1]]}")

        if "delim:not" in pattern_name:
            self.errors.add_minor(f"Missing delimiter after: {chars_subst[_range[0]:_range[1]]}")

        return _range


def split_bracketed_by_comma(text: str, errors: DetectedErrors):
    """ Splits the input text by comma, but only on the top level, ignoring commas inside brackets. Returns the list of split parts. """

    classifier = SplitBacketedByCommaCharacterClassifier()
    tokeniser = SplitBacketedByCommaTokeniser(errors)

    lexer = SimpleLexer(classifier, tokeniser)
    tokens = lexer.parse(text)

    return [t.text for t in tokens]

