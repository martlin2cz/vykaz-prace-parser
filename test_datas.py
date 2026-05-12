from unittest import TestCase

from datas import TaskHoursFlags, TaskHours


class TestTaskHoursFlags(TestCase):

    def test_str(self):
        self.assertEqual(str(TaskHoursFlags(False, False)), "")
        self.assertEqual(str(TaskHoursFlags(True, False)), "?")


class TestTaskHours(TestCase):

    def test_str(self):
        self.assertEqual(str(TaskHours(6, TaskHoursFlags(False, False))), "6")

        self.assertEqual(str(TaskHours(2, TaskHoursFlags(True, False))), "2?")

        self.assertEqual(str(TaskHours(11, TaskHoursFlags(False, True))), "11!")
        self.assertEqual(str(TaskHours(12, TaskHoursFlags(True, True))), "12?!")

        self.assertEqual(str(TaskHours(None, TaskHoursFlags(False, False))), "?")
        self.assertEqual(str(TaskHours(0, TaskHoursFlags(False, False))), "0")
