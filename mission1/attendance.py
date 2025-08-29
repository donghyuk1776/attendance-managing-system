import os
from pathlib import Path
from typing import Any, Mapping, Union


FILENAME = "attendance_weekday_500.txt"
TRAINING_DAYS = ["wednesday"]
MATCH_DAYS = ["saturday", "sunday"]


def read_input_file(filename: Union[Path, str]) -> Mapping[str, Any]:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No filename of {filename}")

    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    data: Mapping[str, Any] = dict()
    count_id = 1

    for line in lines:
        name, day = line.strip().split(" ")
        if name not in data:
            table = {
                "ID": count_id,
                "DAYS": [day],
                "GRADE": None,
                "SCORE": None,
            }
            data[name] = table
            count_id += 1
            continue

        data[name]["DAYS"].append(day)

    return data

def add_score(name_to_table: Mapping[str, Any]) -> Mapping[str, Any]:
    for name, table in name_to_table.items():
        days = table["DAYS"]
        score = 0
        for day in days:
            score += 1
            if day in TRAINING_DAYS:
                score +=  2
            if day in MATCH_DAYS:
                score += 1

        if len([day for day in days if day in TRAINING_DAYS]) >= 10:
            score += 10
        if len([day for day in days if day in MATCH_DAYS]) >= 10:
            score += 10

        name_to_table[name]["SCORE"] = score
        if score < 30:
            grade = "NORMAL"
        elif 30 <= score < 50:
            grade = "SILVER"
        else:
            grade = "GOLD"

        name_to_table[name]["GRADE"] = grade

    return name_to_table

def report(name_to_table: Mapping[str, Any]) -> None:
    max_id = max([table["ID"] for _, table in name_to_table.items()])
    removed = []
    for id_ in range(1, max_id + 1):
        name = [n for n, table in name_to_table.items() if table["ID"] == id_][0]
        table = [table for n, table in name_to_table.items() if table["ID"] == id_][0]
        point = table["SCORE"]
        grade = table["GRADE"]
        print(f"NAME : {name}, POINT : {point}, GRADE : {grade}")

        days = table["DAYS"]
        condition = (
            (grade == "NORMAL")
            and not [day for day in days if day in TRAINING_DAYS + MATCH_DAYS]
        )
        if condition:
            removed.append(name)

    print("\nRemoved player")
    print("==============")
    for r in removed:
        print(r)



if __name__ == "__main__":
    name_to_table = read_input_file(FILENAME)
    name_to_table = add_score(name_to_table)
    report(name_to_table)
    print("")
