from parse import LineParser, FileParser
from parse import LineParts

import unittest
import pathlib

########################################################################################################################


class TestFileParser(unittest.TestCase):

    def test_load_lines(self) -> None:
        path = pathlib.Path("sample_input.txt")
        lines = FileParser._load_lines_(path)

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "23.04.2026 - DOLOREM (lorem) (7)")
        self.assertEqual(lines[1], "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)")

    def test_parse_file(self) -> None:
        path = pathlib.Path("sample_input.txt")
        records = FileParser.parse_file(path)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0], LineParts(date_part="23.04.2026", task_list_part="DOLOREM (lorem)", hours_list_part="7"))
        self.assertEqual(records[1], LineParts(date_part="24.04.2026", task_list_part="DOLOREM (lorem), LIPSUM (ipsum)", hours_list_part="7 + 1"))


class TestLineParser(unittest.TestCase):

    def test_detect_parts_single_standart(self) -> None:
        line = "23.04.2026 - DOLOREM (lorem) (7)"
        parts = LineParser.detect_parts(line)

        self.assertIsNotNone(parts)
        self.assertEqual(parts.date_part, "23.04.2026")
        self.assertEqual(parts.task_list_part, "DOLOREM (lorem)")
        self.assertEqual(parts.hours_list_part, "7")

    def test_detect_parts_multiple_standart(self) -> None:
        line = "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        parts = LineParser.detect_parts(line)

        self.assertIsNotNone(parts)
        self.assertEqual(parts.date_part, "24.04.2026")
        self.assertEqual(parts.task_list_part, "DOLOREM (lorem), LIPSUM (ipsum)")
        self.assertEqual(parts.hours_list_part, "7 + 1")

########################################################################################################################


if __name__ == '__main__':
    unittest.main()