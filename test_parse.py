from parse import LineParser
import unittest

########################################################################################################################


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