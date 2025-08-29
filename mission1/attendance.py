import os
from pathlib import Path
from typing import Any, List, Mapping, Tuple, Union


FILENAME = "attendance_weekday_500.txt"

TRAINING_DAYS = [
    "wednesday",
]

WEEKEND_DAYS = [
    "saturday",
    "sunday",
]

TYPE_INPUT_DATA = List[Tuple[str, str]]

TYPE_TABLE = Mapping[int, Mapping[str, Any]]


def read_input_file(filename: Union[Path, str]) -> TYPE_INPUT_DATA:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No filename of {filename}")

    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    input_data = []
    for line in lines:
        name, day = line.strip().split(" ")
        input_data.append((name, day))

    return input_data


def generate_attendance_table(data: TYPE_INPUT_DATA) -> TYPE_TABLE:
    table: Mapping[int, Mapping[str, Any]] = dict()
    name_to_id: Mapping[str, int] = dict()
    cnt_id = 1
    for (name, day) in data:
        if name not in name_to_id:
            name_to_id[name] = cnt_id
            new = {
                "NAME": name,
                "DAYS": [day],
                "POINT": None,
                "GRADE": None,
            }
            table[cnt_id] = new
            cnt_id += 1
            continue

        id_ = name_to_id[name]
        table[id_]["DAYS"].append(day)

    return table


def update_point(table: TYPE_TABLE) -> TYPE_TABLE:

    def _calculate_daily_point(input_days: List[str]) -> int:
        point = 0
        for day in input_days:
            if day in TRAINING_DAYS:
                point += 3
                continue
            if day in WEEKEND_DAYS:
                point += 2
                continue
            point += 1

        return point

    def _calculate_event_point(input_days: List[str]) -> int:
        point = 0
        training_count = 10
        training_point = 10
        weekend_count = 10
        weekend_point = 10

        if len([day for day in days if day in TRAINING_DAYS]) >= training_count:
            point += training_point

        if len([day for day in days if day in WEEKEND_DAYS]) >= weekend_count:
            point += weekend_point

        return point

    for id_, personal_table in table.items():
        days = personal_table["DAYS"]
        total_point = (
            _calculate_daily_point(days)
            + _calculate_event_point(days)
        )
        personal_table["POINT"] = total_point

    if any([personal_table["POINT"] is None for _, personal_table in table.items()]):
        RuntimeError("Invalid update in point.")

    return table


def update_grade(table: TYPE_TABLE) -> TYPE_TABLE:
    for id_, personal_table in table.items():
        point = personal_table["POINT"]
        if point < 30:
            grade = "NORMAL"
        elif 30 <= point < 50:
            grade = "SILVER"
        else:
            grade = "GOLD"

        personal_table["GRADE"] = grade

    if any([personal_table["GRADE"] is None for _, personal_table in table.items()]):
        RuntimeError("Invalid update in grade.")

    return table


def report(table: TYPE_TABLE) -> None:

    def _check_to_remove(grade_in: str, days_in: List[str]) -> bool:
        flag_remove: bool = (
            (grade_in == "NORMAL")
            & (not [d for d in days_in if d in TRAINING_DAYS + WEEKEND_DAYS])
        )
        return flag_remove

    names_to_remove = []
    for id_, personal_table in table.items():
        name = personal_table["NAME"]
        point = personal_table["POINT"]
        grade = personal_table["GRADE"]
        print(f"NAME : {name}, POINT : {point}, GRADE : {grade}")

        days = personal_table["DAYS"]
        if _check_to_remove(grade, days):
            names_to_remove.append(name)

    print("\nRemoved player")
    print("==============")
    for name in names_to_remove:
        print(name)


if __name__ == "__main__":
    input_data = read_input_file(FILENAME)
    attendance_table = generate_attendance_table(input_data)
    attendance_table = update_point(attendance_table)
    attendance_table = update_grade(attendance_table)
    report(attendance_table)
