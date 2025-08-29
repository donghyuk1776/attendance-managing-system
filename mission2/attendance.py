from attendance_manager import AttendanceManager
from attendance_record import AttendanceRecordLoader
from grade import load_grade
from point import load_point


FILENAME = "attendance_weekday_500.txt"


def main() -> None:
    point = load_point("base")
    grade = load_grade("base")
    records = AttendanceRecordLoader.load(filename=FILENAME)

    manager = AttendanceManager(point=point, grade=grade)
    manager.report(records)


if __name__ == "__main__":
    main()