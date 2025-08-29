import pytest


from attendance_manager import AttendanceManager
from attendance_record import AttendanceRecordLoader, PersonalAttendanceRecord
from grade import load_grade
from point import load_point


def test_loader():
    loader = AttendanceRecordLoader
    with pytest.raises(FileNotFoundError):
        res = loader.load(filename="attendance.txt")

    res = loader.load(filename="mission2/attendance_weekday_500.txt")
    assert isinstance(res[1].name, str)


def test_manager():
    days = [
       "monday",
       "tuesday",
       "wednesday",
       "thursday",
       "friday",
       "saturday",
       "sunday",
    ] * 20
    record_1 = PersonalAttendanceRecord(
        name="Jung",
        identification=1,
        days=days,
    )
    record_2 = PersonalAttendanceRecord(
        name="Kim",
        identification=2,
        days=["tuesday"],
    )
    records = {1: record_1, 2: record_2}

    point = load_point("base")
    grade = load_grade("base")
    manager = AttendanceManager(point, grade)
    manager.report(records)





def test_point_base():
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ] * 20
    record = PersonalAttendanceRecord(
        name="Jung",
        identification=1,
        days=days,
    )
    point = load_point("base")
    res = point.update(record)
    assert res.point ==  240


def test_point_premium():
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ] * 20
    record = PersonalAttendanceRecord(
        name="Jung",
        identification=1,
        days=days,
    )
    point = load_point("premium")
    res = point.update(record)
    assert res.point ==  320


def test_point_factory():
    with pytest.raises(RuntimeError):
        point = load_point("invalid")


def test_grade_base():
    grade = load_grade("base")
    res1 = grade.update(50)
    assert res1 == "GOLD"
    res2 = grade.update(40)
    assert res2 == "SILVER"
    res3 = grade.update(5)
    assert res3 == "NORMAL"

    res4 = grade.check_to_be_removed(
        grade="NORMAL",
        days=["saturday"],
    )
    assert res4 == False


def test_grade_premium():
    grade = load_grade("premium")
    res1 = grade.update(50)
    assert res1 == "GOLD"
    res2 = grade.update(40)
    assert res2 == "SILVER"
    res3 = grade.update(5)
    assert res3 == "NORMAL"
    res4 = grade.update(100)
    assert res4 == "PREMIUM"
    res5 = grade.check_to_be_removed(
        grade="NORMAL",
        days=["saturday"],
    )
    assert res5 == False


def test_grade_factory():
    with pytest.raises(RuntimeError):
        grade = load_grade("invalid")