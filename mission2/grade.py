from abc import ABC, abstractmethod
from typing import List, Type


class GradeAbstract(ABC):

    @classmethod
    @abstractmethod
    def update(cls, point: int) -> str:
        """update grade."""

    @classmethod
    @abstractmethod
    def check_to_be_removed(cls, grade: str, days: List[str]) -> bool:
        """check to be removed person name."""



class GradeBase(GradeAbstract):

    @classmethod
    def update(cls, point: int) -> str:
        if point >= 50:
            return "GOLD"
        if point >= 30:
            return "SILVER"
        return "NORMAL"

    @classmethod
    def check_to_be_removed(cls, grade: str, days: List[str]) -> bool:
        remove_grades: List[str] = ["NORMAL"]
        important_days: List[str] = ["wednesday", "saturday", "sunday"]

        check_grade: bool = grade in remove_grades
        check_days: bool = len([day for day in days if day in important_days]) == 0
        return check_grade & check_days


class GradePremium(GradeAbstract):

    @classmethod
    def update(cls, point: int) -> str:
        if point >= 90:
            return "PREMIUM"
        if point >= 50:
            return "GOLD"
        if point >= 30:
            return "SILVER"
        return "NORMAL"

    @classmethod
    def check_to_be_removed(cls, grade: str, days: List[str]) -> bool:
        remove_grades: List[str] = ["NORMAL"]
        important_days: List[str] = ["wednesday", "saturday", "sunday"]

        check_grade: bool = grade in remove_grades
        check_days: bool = len([day for day in days if day in important_days]) == 0
        return check_grade & check_days



def load_grade(name: str) -> Type[GradeAbstract]:
    name_to_grade = {
        "base": GradeBase,
        "premium": GradePremium,
    }
    try:
        cls = name_to_grade[name]
        return cls

    except KeyError:
        raise RuntimeError(f"Invalid name to load grade: {name}")
