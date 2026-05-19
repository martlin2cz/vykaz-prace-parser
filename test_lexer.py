import re
import typing
from unittest import TestCase

from lexer import AbstractCharacterClassifier, AbstractTokeniser, ClassifiedCharacters, SimpleToken


class TestingCharacterClassifier(AbstractCharacterClassifier):

    def class_of_char(self, i: int, char: str, text: str) -> str:
        if char.isdecimal():
            return "D"
        if char.isalpha():
            return "A"
        if char in ".,;":
            return ","
        if char.isspace():
            return "_"

        return "?" # FIXME yield null


class TestCharacterClassifier(TestCase):
    def test_it(self):
        classifier = TestingCharacterClassifier()

        classes = classifier.classify("foo42, 99.5 BAAR!")
        self.assertEqual(classes.char_classes, "AAADD,_DD,D_AAAA?")


class TestingTokeniser(AbstractTokeniser):

    def __init__(self):
        self.pattern = re.compile(r"(A[AD]+)|(D+)|(,_*)")

    def  find_matching_token(self, char_classes_substr: str) -> re.Match | typing.Tuple[int, int] | None:
        return self.pattern.match(char_classes_substr)


class TestAbstractTokeniser(TestCase):
    def test_it(self):
        tokenizer = TestingTokeniser()

        classes = ClassifiedCharacters("foo42, 99.5 BAAR!", "AAADD,_DD,D_AAAA?")
        tokens = tokenizer.tokenise(classes)
        self.assertEqual(tokens, [
            SimpleToken(start_char_index=0, end_char_index=5, text='foo42'),
            SimpleToken(start_char_index=5, end_char_index=7, text=', '),
            SimpleToken(start_char_index=7, end_char_index=9, text='99'),
            SimpleToken(start_char_index=9, end_char_index=10, text='.'),
            SimpleToken(start_char_index=10, end_char_index=11, text='5'),
            SimpleToken(start_char_index=12, end_char_index=16, text='BAAR')
        ])



class TestSimpleLexer(TestCase):
    def test_parse(self):
        ...
