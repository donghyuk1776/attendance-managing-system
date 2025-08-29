from typing import List, Mapping, Type

from attendance_record import PersonalAttendanceRecord
from grade import GradeAbstract
from point import PointAbstract


TYPE_RECORDS = Mapping[int, PersonalAttendanceRecord]


class AttendanceManager:

    def __init__(
            self,
            point: Type[PointAbstract],
            grade: Type[GradeAbstract],
    ) -> None:
        self.point = point
        self.grade = grade

    def report(self, records: TYPE_RECORDS) -> None:
        records = self._update_score(records)
        records = self._update_grade(records)
        names_to_remove = self._check_to_be_removed(records)
        self._report(records, names_to_remove)

    def _update_score(self, records: TYPE_RECORDS) -> TYPE_RECORDS:
        updated = dict()
        for id_, personal_record in records.items():
            updated[id_] = self.point.update(personal_record)
        return updated

    def _update_grade(self, records: TYPE_RECORDS) -> TYPE_RECORDS:
        updated = dict()
        for id_, personal_record in records.items():
            point = personal_record.point
            grade = self.grade.update(point)
            personal_record.grade = grade
            updated[id_] = personal_record
        return updated

    def _check_to_be_removed(self, records: TYPE_RECORDS) -> List[str]:
        names_to_remove = []
        for id_, personal_record in records.items():
            name = personal_record.name
            grade = personal_record.grade
            days = personal_record.days
            flag_to_remove = self.grade.check_to_be_removed(grade, days)
            if flag_to_remove:
                names_to_remove.append(name)

        return names_to_remove

    def _report(self, records: TYPE_RECORDS, names_to_remove: List[str]) -> None:
        for id_, personal_table in records.items():
            name = personal_table.name
            point = personal_table.point
            grade = personal_table.grade
            print(f"NAME : {name}, POINT : {point}, GRADE : {grade}")

        print("\nRemoved player")
        print("==============")
        for name in names_to_remove:
            print(name)
