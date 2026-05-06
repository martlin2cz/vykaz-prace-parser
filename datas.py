from dataclasses import dataclass, field
from typing import Dict, List


########################################################################################################################


@dataclass(frozen=True)
class LineParts:
    """ Raw parsed line parts. """

    date_part: str
    task_list_part: str
    hours_list_part: str | None
    format_name: str


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


@dataclass
class DetectedErrors:
    """ Mutable container for errors detected during processing. """
    errors: List[str] = field(default_factory=list)

    def add(self, error: str) -> None:
        self.errors.append(error)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def errors_list(self) -> str:
        return ", ".join(self.errors)