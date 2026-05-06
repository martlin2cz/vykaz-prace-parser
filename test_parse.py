from unittest import TestCase

from parse import LineParser, LinesParser, DatePartParser, TasksListParser, HoursListParser, RecordsParser
from datas import DateInfo, TaskInfo, TaskHours, DayRecord, DetectedErrors

import unittest
import pathlib


########################################################################################################################


class TestLinesParser(unittest.TestCase):

    def test_some(self) -> None:
        path = pathlib.Path("sample_input.txt")
        lines = LinesParser.parse_file(path)

        self.assertEqual(lines, [
            "23.04.2026 - DOLOREM (lorem) (7)",
            "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)",
            "05.07.2026 - UNNUNEN (noon) (?)",
            "05.07.2026 - BINUNEN (lesser), SECUNEN (morer), TERNEN (unoko) (3 + 5? + ?)",
            "11.03.2026 - LOLOREM (nohours), BOLIPSUM (nohours too)",
            "12.03.2026 - DONOMEM (nohours singular)",
            "07.09.2026 - MONON (qumun), YUNON (munon) (3)",
            "08.09.2026 - VERYNON (yun) (2 + 4)"
        ])

########################################################################################################################


class TestLineParser(unittest.TestCase):

    def test_detect_parts_single_standart(self) -> None:
        line = "23.04.2026 - DOLOREM (lorem) (7)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertFalse(errors.has_errors())
        self.assertEqual(parts.date_part, "23.04.2026")
        self.assertEqual(parts.task_list_part, "DOLOREM (lorem)")
        self.assertEqual(parts.hours_list_part, "7")

    def test_detect_parts_multiple_standart(self) -> None:
        line = "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertFalse(errors.has_errors())
        self.assertEqual(parts.date_part, "24.04.2026")
        self.assertEqual(parts.task_list_part, "DOLOREM (lorem), LIPSUM (ipsum)")
        self.assertEqual(parts.hours_list_part, "7 + 1")

    def test_detect_parts_unprecise_single(self) -> None:
        line = "05.07.2026 - UNNUNEN (noon) (?)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertFalse(errors.has_errors())
        self.assertEqual(parts.date_part, "05.07.2026")
        self.assertEqual(parts.task_list_part, "UNNUNEN (noon)")
        self.assertEqual(parts.hours_list_part, "?")

    def test_detect_parts_unprecise_multiple(self) -> None:
        line = "05.07.2026 - BINUNEN (lesser), SECUNEN (morer), TERNEN (unoko) (3 + 5? + ?)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertFalse(errors.has_errors())
        self.assertEqual(parts.date_part, "05.07.2026")
        self.assertEqual(parts.task_list_part, "BINUNEN (lesser), SECUNEN (morer), TERNEN (unoko)")
        self.assertEqual(parts.hours_list_part, "3 + 5? + ?")

    def test_detect_parts_nohours_single(self) -> None:
        line = "12.03.2026 - DONOMEM (nohours singular)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertEqual(parts.date_part, "12.03.2026")
        self.assertEqual(parts.task_list_part, "DONOMEM (nohours singular)")
        self.assertEqual(parts.hours_list_part, None)
        self.assertFalse(errors.has_errors())


    def test_detect_parts_nohours_multiple(self) -> None:
        line = "11.03.2026 - LOLOREM (nohours), BOLIPSUM (nohours too)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertEqual(parts.date_part, "11.03.2026")
        self.assertEqual(parts.task_list_part, "LOLOREM (nohours), BOLIPSUM (nohours too)")
        self.assertEqual(parts.hours_list_part, None)
        self.assertFalse(errors.has_errors())


########################################################################################################################


class TestDatePartParser(TestCase):
    def test_some(self):
        date_part = "23.04.2026"
        errors = DetectedErrors()
        date = DatePartParser.detect_date(date_part, errors)

        self.assertFalse(errors.has_errors())
        self.assertEqual(date, DateInfo("23.04.2026"))

########################################################################################################################


class TestTasksListParser(TestCase):
    def test_singular(self):
        tasks_list_part = "DOLOREM (lorem)"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertFalse(errors.has_errors())
        self.assertEqual(tasks, [
            TaskInfo(task_id="DOLOREM", task_text="lorem")
        ])

    def test_multiple(self):
        tasks_list_part = "DOLOREM (lorem), LIPSUM (ipsum)"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertFalse(errors.has_errors())
        self.assertEqual(tasks, [
            TaskInfo(task_id="DOLOREM", task_text="lorem"),
            TaskInfo(task_id="LIPSUM", task_text="ipsum")
        ])


########################################################################################################################


class TestHoursListParser(TestCase):
    def test_singular(self):
        hours_list_part = "7"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertFalse(errors.has_errors())
        self.assertEqual(hours, [
            TaskHours(raw_hours="7")
        ])

    def test_multiple(self):
        hours_list_part = "7 + 1"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertFalse(errors.has_errors())
        self.assertEqual(hours, [
            TaskHours(raw_hours="7"),
            TaskHours(raw_hours="1")
        ])

    def test_absolutelly_unknown(self):
            hours_list_part = "?"
            errors = DetectedErrors()
            hours = HoursListParser.detect_hours(hours_list_part, errors)

            self.assertFalse(errors.has_errors())
            self.assertEqual(hours, [TaskHours(raw_hours="?")])

    def test_some_unknowns(self):
        hours_list_part = "3 + 5? + ?"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertFalse(errors.has_errors())
        self.assertEqual(hours, [
            TaskHours(raw_hours="3"),
            TaskHours(raw_hours="5?"),
            TaskHours(raw_hours="?")
        ])


########################################################################################################################


class TestRecordsParserForLine(TestCase):
    def setUp(self) -> None:
        self.record_parser = RecordsParser()

    def test_some_line(self):
        line = "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        record, errors = self.record_parser.process_line(line)

        self.assertFalse(errors.has_errors())
        self.assertEqual(record, DayRecord(
            date=DateInfo("24.04.2026"),
            tasks={
                TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours(raw_hours="7"),
                TaskInfo(task_id="LIPSUM", task_text="ipsum"): TaskHours(raw_hours="1")
            }
        ))

    def test_fill_missing_hours(self):
        line = "07.09.2026 - MONON (qumun), YUNON (munon) (3)"
        record, errors = self.record_parser.process_line(line)

        self.assertEqual("No hours provided for task: TaskInfo(task_id='YUNON', task_text='munon')", errors.errors_list())
        self.assertEqual(record, DayRecord(
            date=DateInfo("07.09.2026"),
            tasks={
                TaskInfo(task_id="MONON", task_text="qumun"): TaskHours(raw_hours="3"),
                TaskInfo(task_id="YUNON", task_text="munon"): TaskHours(raw_hours="???")
            }
        ))

    def test_fill_missing_tasks(self):
        line = "08.09.2026 - VERYNON (yun) (2 + 4)"
        record, errors = self.record_parser.process_line(line)

        self.assertEqual("Extra hours (missing task): TaskHours(raw_hours='4')", errors.errors_list())
        self.assertEqual(record, DayRecord(
            date=DateInfo("08.09.2026"),
            tasks={
                TaskInfo(task_id="VERYNON", task_text="yun"): TaskHours(raw_hours="2"),
                TaskInfo(task_id="TASK-???", task_text="???"): TaskHours(raw_hours="4")
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
            ),
            DayRecord(
                date=DateInfo("05.07.2026"),
                tasks={
                    TaskInfo(task_id="UNNUNEN", task_text="noon"): TaskHours(raw_hours="?")
                }
            ),
            DayRecord(
                date=DateInfo("05.07.2026"),
                tasks={
                    TaskInfo(task_id="BINUNEN", task_text="lesser"): TaskHours(raw_hours="3"),
                    TaskInfo(task_id="SECUNEN", task_text="morer"): TaskHours(raw_hours="5?"),
                    TaskInfo(task_id="TERNEN", task_text="unoko"): TaskHours(raw_hours="?")
                }
            ),
            DayRecord(
                date=DateInfo("11.03.2026"),
                tasks={
                    TaskInfo(task_id="LOLOREM", task_text="nohours"): TaskHours(raw_hours="8?"),
                    TaskInfo(task_id="BOLIPSUM", task_text="nohours too"): TaskHours(raw_hours="???"),
                }
            ),
            DayRecord(
                date=DateInfo("12.03.2026"),
                tasks={
                    TaskInfo(task_id="DONOMEM", task_text="nohours singular"): TaskHours(raw_hours="8?")
                }
            ),
            DayRecord(
                date=DateInfo(raw_date='07.09.2026'),
                tasks={
                    TaskInfo(task_id='MONON', task_text='qumun'): TaskHours(raw_hours='3'),
                    TaskInfo(task_id='YUNON', task_text='munon'): TaskHours(raw_hours='???')
                }
            ),
            DayRecord(
                date=DateInfo(raw_date='08.09.2026'),
                tasks={
                    TaskInfo(task_id='VERYNON', task_text='yun'): TaskHours(raw_hours='2'),
                    TaskInfo(task_id='TASK-???', task_text='???'): TaskHours(raw_hours='4')
                }
            ),
        ])

########################################################################################################################


if __name__ == '__main__':
    unittest.main()
