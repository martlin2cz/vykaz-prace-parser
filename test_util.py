from typing import List
from unittest import TestCase

import util
from datas import DetectedErrors
from lexer import ClassifiedCharacters, SimpleToken


class TestSplitBacketedByCommaCharacterClassifier(TestCase):
    def test_all(self):
        self._run_test("foo", "TTT")
        self._run_test("lo (rem)", "TTSBBBBB")
        self._run_test("do,lor,sit", "TTDTTTDTTT")

        self._run_test("foo (bar(baz),42), aux;qux", "TTTSBBBBBBBBBBBBBDSTTTTTTT")

    def _run_test(self, text: str, expected_classes: str):
        classifier = util.SplitBacketedByCommaCharacterClassifier()

        self.assertEqual(classifier.classify(text), ClassifiedCharacters(text, expected_classes))


class TestSplitBacketedByCommaTokeniser(TestCase):
    def test_primitive(self):
        self._run_test("foo", "TTT",
                       "",
                       "foo")

    def test_singular(self):
        self._run_test("bar (42)", "TTTSBBBB",
                       "",
                       "bar (42)")

    def test_multiple(self):
        self._run_test("baz (43), BAZ (44)", "TTTSBBBBDSTTTSBBBB",
                       "",
                       "baz (43), ", "BAZ (44)")

    def test_combined(self):
        self._run_test("qux (11), QUUX, quuux (22), QUUUUX", "TTTSBBBBDSTTTTDSTTTTTSBBBBDSTTTTTT",
                       "",
                       "qux (11), ","QUUX, ", "quuux (22), ", "QUUUUX")

    def test_invalid_cases(self):
        self._run_test("qux (11) QUUX quuux (22) (33)", "TTTSBBBBSTTTTSTTTTTSBBBBSBBBB",
                       "Missing delimiter after: qux (11) , Missing delimiter after: QUUX quuux (22) , Invalid task format: (33)",
                       "qux (11) ", "QUUX quuux (22) ", "(33)")



    def _run_test(self, text: str, classes: str, expected_errors: str, *expected_token_texts: List[str]):
        errors = DetectedErrors()
        tokeniser = util.SplitBacketedByCommaTokeniser(errors)

        classified = ClassifiedCharacters(text, classes)
        actual_tokens = tokeniser.tokenise(classified)

        self.assertEqual([t.text for t in actual_tokens], list(expected_token_texts))
        self.assertEqual(expected_errors, str(errors))

