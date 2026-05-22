from unittest import TestCase

from parse import LineParser, LinesParser, DatePartParser, TasksListParser, HoursListParser, RecordsParser
from datas import DateInfo, TaskInfo, TaskHours, TaskHoursFlags, DayRecord, DetectedErrors

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
            "2.2.2026 - TUNRMA (toned) (9)",
            "3. 2. 2026 - DINRMA (moned) (7)",
            "05.07.2026 - UNNUNEN (noon) (?)",
            "05.07.2026 - BINUNEN (lesser), SECUNEN (morer), TERNEN (unoko) (3 + 5? + ?)",
            '12.10.2026 - NORNENER (non), LENENER (len), MORENER (moo) (2 + 3+ + 4-)',
            "11.03.2026 - LOLOREM (nohours), BOLIPSUM (nohours too)",
            "12.03.2026 - DONOMEM (nohours singular)",
            "06.06.2026 - SUNEMEM (7)",
            "07.06.2026 - PUNUMEM, BUNUMEM (6 + 2)",
            "08.06.2026 - DETENM (peen), NOSODNM (3 + 5)",
            "07.09.2026 - MONON (qumun), YUNON (munon) (3)",
            "08.09.2026 - VERYNON (yun) (2 + 4)",
            "14.10.2026 - MILID (sum) NILID (yum) (4 + 6)",
            "15.10.2026 - CORDLY, SIMID SINILID, FUNKDLY (1 + 3 + 2 + 4)"
        ])

########################################################################################################################


class TestLineParser(unittest.TestCase):

    def test_detect_parts_single_standart(self) -> None:
        line = "23.04.2026 - DOLOREM (lorem) (7)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "23.04.2026")
        self.assertEqual(parts.task_list_part, "DOLOREM (lorem)")
        self.assertEqual(parts.hours_list_part, "7")

    def test_detect_parts_multiple_standart(self) -> None:
        line = "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "24.04.2026")
        self.assertEqual(parts.task_list_part, "DOLOREM (lorem), LIPSUM (ipsum)")
        self.assertEqual(parts.hours_list_part, "7 + 1")

    def test_detect_parts_date_format_without_zeros(self) -> None:
        line = "2.2.2026 - TUNRMA (toned) (8)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "2.2.2026")
        self.assertEqual(parts.task_list_part, "TUNRMA (toned)")
        self.assertEqual(parts.hours_list_part, "8")

    def test_detect_parts_date_format_with_spaces(self) -> None:
        line = "3. 2. 2026 - DINRMA (moned) (7)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "3. 2. 2026")
        self.assertEqual(parts.task_list_part, "DINRMA (moned)")
        self.assertEqual(parts.hours_list_part, "7")

    def test_detect_parts_unprecise_single(self) -> None:
        line = "05.07.2026 - UNNUNEN (noon) (?)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "05.07.2026")
        self.assertEqual(parts.task_list_part, "UNNUNEN (noon)")
        self.assertEqual(parts.hours_list_part, "?")

    def test_detect_parts_unprecise_multiple(self) -> None:
        line = "05.07.2026 - BINUNEN (lesser), SECUNEN (morer), TERNEN (unoko) (3 + 5? + ?)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
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
        self.assertTrue(errors.is_ok())

    def test_detect_parts_nohours_multiple(self) -> None:
        line = "11.03.2026 - LOLOREM (nohours), BOLIPSUM (nohours too)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertEqual(parts.date_part, "11.03.2026")
        self.assertEqual(parts.task_list_part, "LOLOREM (nohours), BOLIPSUM (nohours too)")
        self.assertEqual(parts.hours_list_part, None)
        self.assertTrue(errors.is_ok())

    def test_detect_parts_without_task_description_multiple(self) -> None:
        line = "13.03.2026 - BONOMEN, BIPSUM (7 + 2)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "13.03.2026")
        self.assertEqual(parts.task_list_part, "BONOMEN, BIPSUM")
        self.assertEqual(parts.hours_list_part, "7 + 2")

    def test_detect_parts_without_task_description_single(self) -> None:
        line = "14.03.2026 - SINOMEN (9)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "14.03.2026")
        self.assertEqual(parts.task_list_part, "SINOMEN")
        self.assertEqual(parts.hours_list_part, "9")

    def test_detect_parts_edge_missing_comma(self) -> None:
        line = "14.10.2026 - MILID (sum) NILID (yum) (4 + 6)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        # Parts detection should still work (date/tasks/hours extracted) even if tasks list is malformed
        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "14.10.2026")
        self.assertEqual(parts.task_list_part, "MILID (sum) NILID (yum)")
        self.assertEqual(parts.hours_list_part, "4 + 6")

    def test_detect_parts_edge_missing_both_delim_and_parentheses(self) -> None:
        line = "15.10.2026 - CORDLY, SIMID SINILID, FUNKDLY (1 + 3 + 2 + 4)"
        errors = DetectedErrors()
        parser = LineParser()
        parts = parser.detect_parts(line, errors)

        self.assertIsNotNone(parts)
        self.assertTrue(errors.is_ok())
        self.assertEqual(parts.date_part, "15.10.2026")
        self.assertEqual(parts.task_list_part, "CORDLY, SIMID SINILID, FUNKDLY")
        self.assertEqual(parts.hours_list_part, "1 + 3 + 2 + 4")


########################################################################################################################


class TestDatePartParser(TestCase):
    def test_some(self):
        date_part = "23.04.2026"
        errors = DetectedErrors()
        date = DatePartParser.detect_date(date_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(date, DateInfo("23.04.2026"))

########################################################################################################################


class TestTasksListParser(TestCase):
    def test_singular(self):
        tasks_list_part = "DOLOREM (lorem)"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(tasks, [
            TaskInfo(task_id="DOLOREM", task_text="lorem")
        ])

    def test_multiple(self):
        tasks_list_part = "DOLOREM (lorem), LIPSUM (ipsum)"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(tasks, [
            TaskInfo(task_id="DOLOREM", task_text="lorem"),
            TaskInfo(task_id="LIPSUM", task_text="ipsum")
        ])

    def test_simplified_singular(self):
        tasks_list_part = "SUNEMEM"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(tasks, [
            TaskInfo(task_id="SUNEMEM", task_text="???")
        ])

    def test_simplified_multiple(self):
        tasks_list_part = "SUNEMEM, BUNUMEM"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(tasks, [
            TaskInfo(task_id="SUNEMEM", task_text="???"),
            TaskInfo(task_id="BUNUMEM", task_text="???")
        ])

    def test_combine_multiple(self):
        tasks_list_part = "DETENM (peen), NOSODNM"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(tasks, [
            TaskInfo(task_id="DETENM", task_text="peen"),
            TaskInfo(task_id="NOSODNM", task_text="???")
        ])

    def test_invalid_missing_comma(self):
        tasks_list_part = "MILID (sum) NILID (yum)"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertEqual(tasks, [
            TaskInfo(task_id="MILID", task_text="sum"),
            TaskInfo(task_id="NILID", task_text="yum")
        ])
        self.assertEqual(str(errors), "Missing delimiter after: MILID (sum) ")

    def test_invalid_missing_parentheses(self):
        tasks_list_part = "CORDLY, SIMID SINILID, FUNKDLY"
        errors = DetectedErrors()
        parser = TasksListParser()
        tasks = parser.detect_tasks(tasks_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(tasks, [
            TaskInfo(task_id="CORDLY", task_text="???"),
            TaskInfo(task_id="SIMID SINILID", task_text="???"),
            TaskInfo(task_id="FUNKDLY", task_text="???")
        ])


########################################################################################################################


class TestHoursListParser(TestCase):
    def test_singular(self):
        hours_list_part = "7"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(hours, [
            TaskHours.with_hours(7)
        ])

    def test_multiple(self):
        hours_list_part = "7 + 1"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(hours, [
            TaskHours.with_hours(7),
            TaskHours.with_hours(1)
        ])

    def test_absolutelly_unknown(self):
        hours_list_part = "?"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(hours, [
            TaskHours.uncertain()
        ])

    def test_some_unknowns(self):
        hours_list_part = "3 + 5? + ?"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(hours, [
            TaskHours.with_hours(3),
            TaskHours.uncertain(5),
            TaskHours.uncertain()
        ])

    def test_less_and_more_and_uncertains(self):
        hours_list_part = "2 + 3+ + 4- + 5-? + 6-? + 7?"
        errors = DetectedErrors()
        hours = HoursListParser.detect_hours(hours_list_part, errors)

        self.assertTrue(errors.is_ok())
        self.assertEqual(hours, [
            TaskHours.with_hours(2),
            TaskHours.not_exact(3, little_more=True),
            TaskHours.not_exact(4, little_less=True),
            TaskHours.not_exact(5, little_less=True, uncertain=True),
            TaskHours.not_exact(6, little_less=True, uncertain=True),
            TaskHours.uncertain(7)
        ])

    def test_parse_hours_flags_valid_cases(self):
        self.assertEqual(HoursListParser._parse_hours_flags(""), TaskHoursFlags(False, False, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("-"), TaskHoursFlags(True, False, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("+"), TaskHoursFlags(False, True, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("?"), TaskHoursFlags(False, False, True, False))
        self.assertEqual(HoursListParser._parse_hours_flags("+?"), TaskHoursFlags(False, True, True, False))
        self.assertEqual(HoursListParser._parse_hours_flags("-?"), TaskHoursFlags(True, False, True, False))

    def test_parse_hours_flags_invalid_cases(self):
        self.assertEqual(HoursListParser._parse_hours_flags("--"), TaskHoursFlags(True, False, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("++"), TaskHoursFlags(False, True, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("???"), TaskHoursFlags(False, False, True, False))
        self.assertEqual(HoursListParser._parse_hours_flags("+-"), TaskHoursFlags(True, True, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("-+"), TaskHoursFlags(True, True, False, False))
        self.assertEqual(HoursListParser._parse_hours_flags("!"), TaskHoursFlags(False, False, False, False))

    def test_parse_hours_valid_cases(self):
        self.assertEqual(HoursListParser._parse_hours("8"), TaskHours.with_hours(8))
        self.assertEqual(HoursListParser._parse_hours("7-"), TaskHours.not_exact(7, little_less=True))
        self.assertEqual(HoursListParser._parse_hours("6+"), TaskHours.not_exact(6, little_more=True))
        self.assertEqual(HoursListParser._parse_hours("?"), TaskHours.uncertain())
        self.assertEqual(HoursListParser._parse_hours("5?"), TaskHours.uncertain(5))

        self.assertEqual(HoursListParser._parse_hours("4+?"), TaskHours.not_exact(4, little_more=True, uncertain=True))
        self.assertEqual(HoursListParser._parse_hours("3-?"), TaskHours.not_exact(3, little_less=True, uncertain=True))

        self.assertEqual(HoursListParser._parse_hours("11"), TaskHours.with_hours(11))
        self.assertEqual(HoursListParser._parse_hours("0"), TaskHours.with_hours(0))

    def test_parse_hours_invalid_cases(self):
        self.assertEqual(HoursListParser._parse_hours("x"), TaskHours(None, TaskHoursFlags(False, False, False, False)))
        self.assertEqual(HoursListParser._parse_hours("y+"), TaskHours(None, TaskHoursFlags(False, True, False, False)))
        self.assertEqual(HoursListParser._parse_hours("Z?"), TaskHours(None, TaskHoursFlags(False, False, True, False)))

        self.assertEqual(HoursListParser._parse_hours("9--"), TaskHours(9, TaskHoursFlags(True, False, False, False)))
        self.assertEqual(HoursListParser._parse_hours("8+-!"), TaskHours(8, TaskHoursFlags(True, True, False, False)))

        self.assertEqual(HoursListParser._parse_hours("-1"), TaskHours(None, TaskHoursFlags(False, False, False, False)))
        self.assertEqual(HoursListParser._parse_hours("4.5"), TaskHours(None, TaskHoursFlags(False, False, False, False)))


########################################################################################################################


class TestRecordsParserForLine(TestCase):
    def setUp(self) -> None:
        self.record_parser = RecordsParser()

    def test_some_line(self):
        line = "24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)"
        record, errors = self.record_parser.process_line(line)

        self.assertTrue(errors.is_ok())
        self.assertEqual(record, DayRecord(
            date=DateInfo("24.04.2026"),
            tasks={
                TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours.with_hours(7),
                TaskInfo(task_id="LIPSUM", task_text="ipsum"): TaskHours.with_hours(1)
            }
        ))

    def test_fill_missing_hours(self):
        line = "07.09.2026 - MONON (qumun), YUNON (munon) (3)"
        record, errors = self.record_parser.process_line(line)

        self.assertEqual("No hours provided for task: TaskInfo(task_id='YUNON', task_text='munon')", str(errors))
        self.assertEqual(record, DayRecord(
            date=DateInfo("07.09.2026"),
            tasks={
                TaskInfo(task_id="MONON", task_text="qumun"): TaskHours.with_hours(3),
                TaskInfo(task_id="YUNON", task_text="munon"): TaskHours.synthetic()
            }
        ))

    def test_fill_missing_tasks(self):
        line = "08.09.2026 - VERYNON (yun) (2 + 4)"
        record, errors = self.record_parser.process_line(line)

        self.assertEqual("Extra hours (missing task): 4", str(errors))
        self.assertEqual(record, DayRecord(
            date=DateInfo("08.09.2026"),
            tasks={
                TaskInfo(task_id="VERYNON", task_text="yun"): TaskHours.with_hours(2),
                TaskInfo(task_id="TASK-???", task_text="???"): TaskHours.with_hours(4)
            }
        ))

    def test_edge_missing_comma(self):
        line = "14.10.2026 - MILID (sum) NILID (yum) (4 + 6)"
        record, errors = self.record_parser.process_line(line)

        self.assertFalse(errors.is_ok())
        self.assertEqual(str(errors), "Missing delimiter after: MILID (sum) ")
        self.assertEqual(record, DayRecord(
            date=DateInfo("14.10.2026"),
            tasks={
                TaskInfo(task_id="MILID", task_text="sum"): TaskHours.with_hours(4),
                TaskInfo(task_id="NILID", task_text="yum"): TaskHours.with_hours(6)
            }
        ))

    def test_edge_missing_both_delim_and_parentheses(self):
        line = "15.10.2026 - CORDLY, SIMID SINILID, FUNKDLY (1 + 3 + 2 + 4)"
        record, errors = self.record_parser.process_line(line)

        self.assertFalse(errors.is_ok())
        self.assertEqual(str(errors), "Extra hours (missing task): 4")
        self.assertEqual(record, DayRecord(
            date=DateInfo("15.10.2026"),
            tasks={
                TaskInfo(task_id="CORDLY", task_text="???"): TaskHours.with_hours(1),
                TaskInfo(task_id="SIMID SINILID", task_text="???"): TaskHours.with_hours(3),
                TaskInfo(task_id="FUNKDLY", task_text="???"): TaskHours.with_hours(2),
                TaskInfo(task_id="TASK-???", task_text="???"): TaskHours.with_hours(4)
            }
        ))


########################################################################################################################


class TestRecordsParserForFile(TestCase):
    def test_some_file(self):

        path = pathlib.Path("sample_input.txt")
        record_parser = RecordsParser()
        records = record_parser.process_file(path)

        expected_records = [
            DayRecord(
                date=DateInfo("23.04.2026"),
                tasks={
                    TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours.with_hours(7)
                }
            ),
            DayRecord(
                date=DateInfo("24.04.2026"),
                tasks={
                    TaskInfo(task_id="DOLOREM", task_text="lorem"): TaskHours.with_hours(7),
                    TaskInfo(task_id="LIPSUM", task_text="ipsum"): TaskHours.with_hours(1)
                }
            ),

            DayRecord(
                date=DateInfo("2.2.2026"),
                tasks={
                    TaskInfo(task_id="TUNRMA", task_text="toned"): TaskHours.with_hours(9)
                }
            ),
            DayRecord(
                date=DateInfo("3. 2. 2026"),
                tasks={
                    TaskInfo(task_id="DINRMA", task_text="moned"): TaskHours.with_hours(7)
                }
            ),

            DayRecord(
                date=DateInfo("05.07.2026"),
                tasks={
                    TaskInfo(task_id="UNNUNEN", task_text="noon"): TaskHours.uncertain()
                }
            ),
            DayRecord(
                date=DateInfo("05.07.2026"),
                tasks={
                    TaskInfo(task_id="BINUNEN", task_text="lesser"): TaskHours.with_hours(3),
                    TaskInfo(task_id="SECUNEN", task_text="morer"): TaskHours.uncertain(5),
                    TaskInfo(task_id="TERNEN", task_text="unoko"): TaskHours.uncertain()
                }
            ),
            DayRecord(
                date=DateInfo("12.10.2026"),
                tasks={
                    TaskInfo(task_id="NORNENER", task_text="non"): TaskHours.with_hours(2),
                    TaskInfo(task_id="LENENER", task_text="len"): TaskHours.not_exact(3, little_more=True),
                    TaskInfo(task_id="MORENER", task_text="moo"): TaskHours.not_exact(4, little_less=True)
                }
            ),
            DayRecord(
                date=DateInfo("11.03.2026"),
                tasks={
                    TaskInfo(task_id="LOLOREM", task_text="nohours"): TaskHours.synthetic(8),
                    TaskInfo(task_id="BOLIPSUM", task_text="nohours too"): TaskHours.synthetic()
                }
            ),
            DayRecord(
                date=DateInfo("12.03.2026"),
                tasks={
                    TaskInfo(task_id="DONOMEM", task_text="nohours singular"): TaskHours.synthetic(8)
                }
            ),
            DayRecord(
                date=DateInfo("06.06.2026"),
                tasks={
                    TaskInfo(task_id="SUNEMEM", task_text="???"): TaskHours.with_hours(7),
                }
            ),
            DayRecord(
                date=DateInfo("07.06.2026"),
                tasks={
                    TaskInfo(task_id="PUNUMEM", task_text="???"): TaskHours.with_hours(6),
                    TaskInfo(task_id="BUNUMEM", task_text="???"): TaskHours.with_hours(2)
                }
            ),
            DayRecord(
                date=DateInfo("08.06.2026"),
                tasks={
                    TaskInfo(task_id="DETENM", task_text="peen"): TaskHours.with_hours(3),
                    TaskInfo(task_id="NOSODNM", task_text="???"): TaskHours.with_hours(5)
                }
            ),
            DayRecord(
                date=DateInfo(raw_date='07.09.2026'),
                tasks={
                    TaskInfo(task_id='MONON', task_text='qumun'): TaskHours.with_hours(3),
                    TaskInfo(task_id='YUNON', task_text='munon'): TaskHours.synthetic()
                }
            ),
            DayRecord(
                date=DateInfo(raw_date='08.09.2026'),
                tasks={
                    TaskInfo(task_id='VERYNON', task_text='yun'): TaskHours.with_hours(2),
                    TaskInfo(task_id='TASK-???', task_text='???'): TaskHours.with_hours(4)
                }
            ),
            DayRecord(
                date=DateInfo("14.10.2026"),
                tasks={
                    TaskInfo(task_id="MILID", task_text="sum"): TaskHours.with_hours(4),
                    TaskInfo(task_id="NILID", task_text="yum"): TaskHours.with_hours(6)
                }
            ),
            DayRecord(
                date=DateInfo("15.10.2026"),
                tasks={
                    TaskInfo(task_id="CORDLY", task_text="???"): TaskHours.with_hours(1),
                    TaskInfo(task_id="SIMID SINILID", task_text="???"): TaskHours.with_hours(3),
                    TaskInfo(task_id="FUNKDLY", task_text="???"): TaskHours.with_hours(2),
                    TaskInfo(task_id="TASK-???", task_text="???"): TaskHours.with_hours(4)
                }
            )
        ]

        self.assertEqual([e.date for e in expected_records], [e.date for e in records])

        for expected_record, actual_record in zip(expected_records, records):
            self.assertEqual(expected_record, actual_record)


########################################################################################################################


if __name__ == '__main__':
    unittest.main()
