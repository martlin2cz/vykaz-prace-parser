from dataclasses import dataclass
from typing import Dict


########################################################################################################################


@dataclass(frozen=True)
class LineParts:
    """ Raw parsed line parts. """

    date_part: str
    task_list_part: str
    hours_list_part: str


@dataclass(frozen=True)
class DateInfo:
    """ The information about the date. """
    raw_date: str


@dataclass(frozen=True)
class TaskInfo:
    """ The information about the task. """
    task_id: str
    task_text: str


@dataclass(frozen=True)
class TaskHours:
    """ The information about the hours spent on a task. """
    raw_hours: str


@dataclass(frozen=True)
class DayRecord:
    """ The information about single day record, with all its tasks. """
    date: DateInfo
    tasks: Dict[TaskInfo, TaskHours]
