from typing import List, Optional, Dict, Tuple
import re
import logging

import pathlib

from datas import LineParts, DateInfo, TaskInfo, TaskHours, DayRecord, DetectedErrors


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

    @staticmethod
    def detect_parts(line: str, errors: DetectedErrors) -> Optional[LineParts]:
        """
        Detects date, task list, and hours list sections from an input line.
        """
        pattern = re.compile(
            r"^(?P<date>\d{2}\.\d{2}\.\d{4})\s+-\s+"
            r"(?P<tasks>.+?)\s*"
            r"\((?P<hours>[^)]+)\)$"
        )

        match = pattern.match(line)

        if not match:
            errors.add("Failed to detect parts")
            return None

        return LineParts(
            date_part=match.group("date"),
            task_list_part=match.group("tasks"),
            hours_list_part=match.group("hours"),
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

    @staticmethod
    def detect_tasks(task_list_part: str, errors: DetectedErrors) -> Optional[List[TaskInfo]]:
        """
        Parses task ID and task text pairs from the task list section.
        """
        task_pattern = re.compile(
            r"\s*(?P<id>[^,(]+)\s*\((?P<text>[^)]+)\)\s*"
        )

        tokens = [t.strip() for t in task_list_part.split(",")]
        tasks: List[TaskInfo] = []

        for token in tokens:
            match = task_pattern.fullmatch(token)
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

    @staticmethod
    def detect_hours(hours_part: str, errors: DetectedErrors) -> List[TaskHours]:
        """
        Parses raw hours tokens from the hours list section.
        """
        return [
            TaskHours(raw_hours=h.strip())
            for h in hours_part.split("+")
            if h.strip()
        ]

########################################################################################################################


class RecordsParser:
    """ The record parser. Parses the input file into a list of DayRecord structures. """

    def __init__(self):
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

        hours = self.hours_list_parser.detect_hours(parts.hours_list_part, errors)

        if len(tasks) != len(hours):
            errors.add(f"Task/hour count mismatch: {line}")
            return None, errors

        task_map: Dict[TaskInfo, TaskHours] = {
            task: hour for task, hour in zip(tasks, hours)
        }

        record = DayRecord(date=date, tasks=task_map)
        return record, errors


########################################################################################################################



