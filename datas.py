from dataclasses import dataclass


########################################################################################################################


@dataclass(frozen=True)
class LineParts:
    """ Raw parsed line parts. """

    date_part: str
    task_list_part: str
    hours_list_part: str

