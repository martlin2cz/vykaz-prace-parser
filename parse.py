from itertools import zip_longest
from typing import List, Optional, Dict, Tuple
import re
import logging

import pathlib
from collections import OrderedDict

import util
from datas import LineParts, DateInfo, TaskInfo, TaskHours, DayRecord, DetectedErrors, TaskHoursFlags


########################################################################################################################


class LinesParser:
    """ The file lines parser. Parses the file into lines. """

    @staticmethod
    def parse_file(path: pathlib.Path) -> List[str]:
        """
        Parses the file content into a list of LineParts.
        """

        lines = LinesParser._load_lines_(path)
        return [line for line in lines if line]

    @staticmethod
    def _load_lines_(path: pathlib.Path) -> List[str]:
        """
        Loads all lines from a text.
        """
        with open(path, "r") as fh:
            return [line.strip() for line in fh]

########################################################################################################################


class LineParser:
    """ The line parser. Parses the line into its parts: date, task list, and hours list. """

    def __init__(self):
        date_part_pattern = r"(?P<date>\d{2}\.\d{2}\.\d{4})"
        tasks_part_pattern = r"(?P<tasks>.+?)"
        hours_part_pattern = r"\((?P<hours>[\d\s+?]+)\)"

        standart_pattern = re.compile(r"^\s*" + date_part_pattern + r"\s+-\s+" + tasks_part_pattern + r"\s*" + hours_part_pattern + r"\s*$")
        nohours_pattern = re.compile(r"^\s*" + date_part_pattern + r"\s+-\s+" + tasks_part_pattern +  r"\s*$")

        self.patterns = OrderedDict([("standart", standart_pattern), ("nohours", nohours_pattern)])

    def detect_parts(self, line: str, errors: DetectedErrors) -> Optional[LineParts]:
        """
        Detects date, task list, and hours list sections from an input line.
        """
        matches, format_name = util.find_match(line, self.patterns)
        if not matches:
            errors.add("Failed to detect parts")
            return None

        return LineParts(
            date_part=matches.get("date", "???"),
            task_list_part=matches.get("tasks", ""),
            hours_list_part=matches.get("hours", None),
            format_name=format_name
        )

########################################################################################################################


class DatePartParser:
    """ The date part parser. Parses the date part into a DateInfo. """

    @staticmethod
    def detect_date(date_part: str, errors: DetectedErrors) -> DateInfo:
        """
        Extracts raw date from detected line parts.
        """
        return DateInfo(raw_date=date_part)

########################################################################################################################


class TasksListParser:
    """ The tasks list parser. Parses the task list part into a list of TaskInfo. """

    def __init__(self):
        task_id_pattern = r"(?P<id>[^,(]+)"
        task_text_pattern = r"(?P<text>[^)]+)"

        self.task_pattern = re.compile(r"\s*" + task_id_pattern + r"\s*\(" + task_text_pattern + r"\s*\)\s*")

    def detect_tasks(self, task_list_part: str, errors: DetectedErrors) -> Optional[List[TaskInfo]]:
        """
        Parses task ID and task text pairs from the task list section.
        """
        tokens = [t.strip() for t in task_list_part.split(",")]
        tasks: List[TaskInfo] = []

        for token in tokens:
            match = self.task_pattern.fullmatch(token)
            if not match:
                errors.add(f"Invalid task format: {token}")
                return None
            tasks.append(
                TaskInfo(
                    task_id=match.group("id").strip(),
                    task_text=match.group("text").strip(),
                )
            )

        return tasks

########################################################################################################################


class HoursListParser:
    """ The hours list parser. Parses the hours list part into a list of TaskHours. """

    TASK_HOURS_PATTERN = re.compile(r"^(?P<hours>[^?!]*)?(?P<flags>[?!]*)$")

    @staticmethod
    def detect_hours(hours_part: str, errors: DetectedErrors) -> List[TaskHours]:
        """
        Parses raw hours tokens from the hours list section.
        """
        return [
            HoursListParser._parse_hours(h.strip())
            for h in hours_part.split("+")
            if h.strip()
        ]

    @staticmethod
    def _parse_hours(task_hours_part: str) -> "TaskHours":
        """ Creates TaskHours from the hours part. """

        matches = HoursListParser.TASK_HOURS_PATTERN.match(task_hours_part)

        hours_part = matches.group("hours") if matches and matches.group("hours") else None
        hours_count = int(hours_part) if hours_part and hours_part.isdecimal() else None

        flags_part = matches.group("flags") if matches and matches.group("flags") else None
        flags = HoursListParser._parse_hours_flags(flags_part) if flags_part else TaskHoursFlags()

        return TaskHours(hours=hours_count, flags=flags)

    @staticmethod
    def _parse_hours_flags(task_hours_flags_part: str) -> "TaskHoursFlags":
        """ Creates TaskHoursFlags from the hours part. """
        return TaskHoursFlags(
            uncertain="?" in task_hours_flags_part,
            synthetic=False
        )

########################################################################################################################


class RecordsParser:
    """ The record parser. Parses the input file into a list of DayRecord structures. """

    def __init__(self):
        self.DEFAULT_HOURS = TaskHours.synthetic(8)

        self.lines_parser = LinesParser()
        self.parts_parser = LineParser()
        self.date_part_parser = DatePartParser()
        self.tasks_list_parser = TasksListParser()
        self.hours_list_parser = HoursListParser()

    def process_file(self, path: pathlib.Path) -> List[DayRecord]:
        """
        Processes the input file into a list of DayRecord structures.
        """
        lines = self.lines_parser.parse_file(path)
        records: List[DayRecord] = []

        for line in lines:
            record, errors = self.process_line(line)
            line_identifier = record.date.raw_date if (record and record.date and record.date.raw_date) else line

            if not errors.has_errors():
                logging.info("%s OK", line_identifier)
            else:
                logging.error("%s: %s", line_identifier, errors.errors_list())

            if record:
                 records.append(record)

        return records

    def process_line(self, line: str) -> Tuple[Optional[DayRecord], DetectedErrors]:
        """
        Processes a single input line into a DayRecord structure.
        """
        errors = DetectedErrors()

        parts = self.parts_parser.detect_parts(line, errors)
        if not parts:
            return None, errors

        date = self.date_part_parser.detect_date(parts.date_part, errors)
        tasks = self.tasks_list_parser.detect_tasks(parts.task_list_part, errors)
        if tasks is None:
            return None, errors

        if parts.hours_list_part is not None:
            hours = self.hours_list_parser.detect_hours(parts.hours_list_part, errors)
        else:
            hours = [self.DEFAULT_HOURS]

        task_map = self._map_tasks_to_hours(tasks, hours, errors)

        record = DayRecord(date=date, tasks=task_map)
        return record, errors

    @staticmethod
    def _map_tasks_to_hours(tasks: List[TaskInfo], hours: List[TaskHours], errors: DetectedErrors) -> Dict[TaskInfo, TaskHours]:
        """ Maps tasks to hours, ensuring that each task has a corresponding hours entry.
        If there are more tasks than hours, the remaining tasks will be mapped to ??? object. """

        result = {}
        for task, hour in zip_longest(tasks, hours, fillvalue=None):
            if task is None:
                errors.add(f"Extra hours (missing task): {hour}")
                task = TaskInfo(task_id="TASK-???", task_text="???")

            if hour is None:
                errors.add(f"No hours provided for task: {task}")
                hour = TaskHours.synthetic()

            result[task] = hour

        return result


########################################################################################################################

