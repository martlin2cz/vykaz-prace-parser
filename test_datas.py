from unittest import TestCase

from datas import TaskHoursFlags, TaskHours


class TestTaskHoursFlags(TestCase):

    def test_str(self):
        self.assertEqual(str(TaskHoursFlags(False, False, False, False)), "")
        self.assertEqual(str(TaskHoursFlags(True, False, False, False)), "-")
        self.assertEqual(str(TaskHoursFlags(False, True, False, False)), "+")
        self.assertEqual(str(TaskHoursFlags(False, False, True, False)), "?")
        self.assertEqual(str(TaskHoursFlags(True, False, True, False)), "-?")
        self.assertEqual(str(TaskHoursFlags(False, True, True, False)), "+?")
        self.assertEqual(str(TaskHoursFlags(True, True, True, True)), "-+?!")


class TestTaskHours(TestCase):

    def test_str(self):
        self.assertEqual(str(TaskHours(6, TaskHoursFlags(False, False, False, False))), "6")
        self.assertEqual(str(TaskHours(7, TaskHoursFlags(False, True, False, False))), "7+")
        self.assertEqual(str(TaskHours(8, TaskHoursFlags(True, False, False, False))), "8-")

        self.assertEqual(str(TaskHours(2, TaskHoursFlags(False, False, True, False))), "2?")
        self.assertEqual(str(TaskHours(3, TaskHoursFlags(True, False, True, False))), "3-?")
        self.assertEqual(str(TaskHours(4, TaskHoursFlags(False, True, True, False))), "4+?")

        self.assertEqual(str(TaskHours(11, TaskHoursFlags(False, False, False, True))), "11!")
        self.assertEqual(str(TaskHours(12, TaskHoursFlags(False, False, True, True))), "12?!")
        self.assertEqual(str(TaskHours(13, TaskHoursFlags(True, False, True, True))), "13-?!")
        self.assertEqual(str(TaskHours(14, TaskHoursFlags(False, True, True, True))), "14+?!")

        self.assertEqual(str(TaskHours(None, TaskHoursFlags(False, False, False, False))), "?")
        self.assertEqual(str(TaskHours(0, TaskHoursFlags(False, False, False, False))), "0")
