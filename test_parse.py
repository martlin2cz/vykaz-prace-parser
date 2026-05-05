from unittest import TestCase

from parse import LineParser, LinesParser, DatePartParser, TasksListParser, HoursListParser, RecordsParser
from datas import DateInfo, TaskInfo, TaskHours, DayRecord

import unittest
import pathlib


########################################################################################################################


class TestLinesParser(unittest.TestCase):

    def test_some(self) -> None:
        path = pathlib.Path("sample_input.txt")
        lines = LinesParser.parse_file(path)

        self.assertEqual(lines, [
            "23.04.2026 - DOLOREM (lorem) (7)",
            "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        ])

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


class TestDatePartParser(TestCase):
    def test_some(self):
        date_part = "23.04.2026"
        date = DatePartParser.detect_date(date_part)

        self.assertEqual(date, DateInfo("23.04.2026"))

########################################################################################################################


class TestTasksListParser(TestCase):
    def test_singular(self):
        tasks_list_part = "DOLOREM (lorem)"
        date = TasksListParser.detect_tasks(tasks_list_part)

        self.assertEqual(date, [
            TaskInfo(task_id="DOLOREM", task_text="lorem")
        ])

    def test_multiple(self):
        tasks_list_part = "DOLOREM (lorem), LIPSUM (ipsum)"
        date = TasksListParser.detect_tasks(tasks_list_part)

        self.assertEqual(date, [
            TaskInfo(task_id="DOLOREM", task_text="lorem"),
            TaskInfo(task_id="LIPSUM", task_text="ipsum")
        ])


########################################################################################################################


class TestHoursListParser(TestCase):
    def test_singular(self):
        hours_list_part = "7"
        hours = HoursListParser.detect_hours(hours_list_part)

        self.assertEqual(hours, [
            TaskHours(raw_hours="7")
        ])

    def test_multiple(self):
        hours_list_part = "7 + 1"
        hours = HoursListParser.detect_hours(hours_list_part)

        self.assertEqual(hours, [
            TaskHours(raw_hours="7"),
            TaskHours(raw_hours="1")
        ])


########################################################################################################################


class TestRecordsParserForLine(TestCase):
    def setUp(self) -> None:
        self.record_parser = RecordsParser()

    def test_some_line(self):
        line = "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        record = self.record_parser.process_line(line)

        self.assertEqual(record, DayRecord(
            date=DateInfo("24.04.2026"),
            tasks={
                TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours(raw_hours="7"),
                TaskInfo(task_id="LIPSUM", task_text="ipsum"): TaskHours(raw_hours="1")
            }
        ))

########################################################################################################################


class TestRecordsParserForFile(TestCase):

    def test_some_file(self):

        path = pathlib.Path("sample_input.txt")
        record_parser = RecordsParser()
        records = record_parser.process_file(path)

        self.assertEqual(records, [
            DayRecord(
                date=DateInfo("23.04.2026"),
                tasks={
                    TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours(raw_hours="7")
                }
            ),
            DayRecord(
                date=DateInfo("24.04.2026"),
                tasks={
                    TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours(raw_hours="7"),
                    TaskInfo(task_id="LIPSUM", task_text="ipsum"): TaskHours(raw_hours="1")
                }
            )
        ])

########################################################################################################################


if __name__ == '__main__':
    unittest.main()


