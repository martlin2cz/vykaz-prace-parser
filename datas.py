from builtins import set
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
class TaskHoursFlags:
    """ The addidional flags related to the hours spent on a task. """
    little_less: bool = False
    little_more: bool = False
    uncertain: bool = False
    synthetic: bool = False

    def __bool__(self):
        return self.little_less or self.little_more or self.uncertain or self.synthetic

    def __str__(self):
        flags = []
        if self.little_less:
            flags.append("-")
        if self.little_more:
            flags.append("+")
        if self.uncertain:
            flags.append("?")
        if self.synthetic:
            flags.append("!")
        return "".join(flags)


@dataclass(frozen=True)
class TaskHours:
    """ The information about the hours spent on a task. """

    hours: int | None
    flags: TaskHoursFlags

    @staticmethod
    def with_hours(hours: int) -> "TaskHours":
        """ Convinience method creating standard TaskHours with the given number of hours. """
        return TaskHours(hours=hours, flags=TaskHoursFlags())

    @staticmethod
    def not_exact(hours: int, little_less: bool = False, little_more: bool = False, uncertain: bool = False) -> "TaskHours":
        """ Convinience method creating a TaskHours with the given number of hours and the little less/more flags. """
        return TaskHours(hours=hours, flags=TaskHoursFlags(little_less=little_less, little_more=little_more, uncertain=uncertain))

    @staticmethod
    def uncertain(hours: int | None = None) -> "TaskHours":
        """ Convinience method creating a TaskHours with the uncertain number of hours (if any). """
        return TaskHours(hours=hours, flags=TaskHoursFlags(uncertain=True))

    @staticmethod
    def synthetic(hours: int | None = None) -> "TaskHours":
        """ Convinience method creating a synthetic TaskHours with the optional hours. """
        return TaskHours(hours=hours, flags=TaskHoursFlags(uncertain=True, synthetic=True))

    def __str__(self):
        hours_str = str(self.hours) if (self.hours is not None) else ("? " if self.flags else "?")
        return f"{hours_str}{self.flags}"


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