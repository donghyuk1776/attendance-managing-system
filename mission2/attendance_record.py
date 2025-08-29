import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping, Optional, Tuple, Union


TYPE_INPUT_DATA = List[Tuple[str, str]]


@dataclass
class PersonalAttendanceRecord:
    name: str
    identification: int
    days: List[str]
    point: Optional[int] = None
    grade: Optional[str] = None
    is_remove_candidate: bool = False

    def update_day_record(self, day: str) -> None:
        self.days.append(day)


class AttendanceRecordLoader:

    @classmethod
    def load(cls, filename: Union[Path, str]) -> Mapping[int, PersonalAttendanceRecord]:
        data = cls._load_input_data(filename=filename)
        records = dict()
        name_to_id: Mapping[str, int] = dict()
        cnt_id = 1
        for (name, day) in data:
            if name not in name_to_id:
                name_to_id[name] = cnt_id
                personal_record = PersonalAttendanceRecord(
                    name=name,
                    identification=cnt_id,
                    days=[day],
                )
                records[cnt_id] = personal_record
                cnt_id += 1
                continue

            id_ = name_to_id[name]
            records[id_].update_day_record(day)

        return records

    @classmethod
    def _load_input_data(cls, filename: Union[Path, str]) -> TYPE_INPUT_DATA:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No filename of {filename}")

        with open(filename, encoding="utf-8") as f:
            lines = f.readlines()

        input_data = []
        for line in lines:
            name, day = line.strip().split(" ")
            input_data.append((name, day))

        return input_data
