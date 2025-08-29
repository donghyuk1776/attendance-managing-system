from abc import ABC, abstractmethod
from typing import List, Type
from attendance_record import PersonalAttendanceRecord


DAYS : List[str] = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


class PointAbstract(ABC):

    @classmethod
    @abstractmethod
    def update(cls, record: PersonalAttendanceRecord) -> PersonalAttendanceRecord:
        """update point."""


class PointBase(PointAbstract):

    training_days: List[str] = [
        "wednesday",
    ]
    weekend_days: List[str] = [
        "saturday",
        "sunday",
    ]

    @classmethod
    def update(cls, record: PersonalAttendanceRecord) -> PersonalAttendanceRecord:
        days = record.days
        point = 0
        point += cls._calculate_daily_point(days)
        point += cls._calculate_event_point(days)
        record.point = point
        return record

    @classmethod
    def _calculate_daily_point(cls, days: List[str]) -> int:
        point = 0
        for day in days:
            if day in cls.training_days:
                point += 3
                continue
            if day in cls.weekend_days:
                point += 2
                continue
            point += 1

        return point

    @classmethod
    def _calculate_event_point(cls, days: List[str]) -> int:
        training_count = 10
        training_point = 10
        weekend_count = 10
        weekend_point = 10

        point = 0
        if len([day for day in days if day in cls.training_days]) >= training_count:
            point += training_point

        if len([day for day in days if day in cls.weekend_days]) >= weekend_count:
            point += weekend_point

        return point


class PointPremium(PointBase):
    training_days: List[str] = [
        "monday",
        "wednesday",
        "friday",
    ]
    weekend_days: List[str] = [
        "saturday",
        "sunday",
    ]


def load_point(name: str) -> Type[PointAbstract]:
    name_to_point = {
        "base": PointBase,
        "premium": PointPremium,
    }
    try:
        cls = name_to_point[name]
        return cls

    except KeyError:
        raise RuntimeError(f"Invalid name to load point: {name}")
