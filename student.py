from functools import reduce
from typing import Dict, List, Tuple, Optional

class Student:
    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id: str = student_id
        self.name: str = name
        self.age: int = age
        self.grades: Dict[str, float] = {}
        self.attendance: int = 0
        self.total_classes: int = 0

    def __str__(self) -> str:
        return f"[{self.student_id}] {self.name} (Age: {self.age})"

    def __repr__(self) -> str:
        return f"Student({self.student_id}, {self.name}, {self.age})"

    def add_grade(self, subject: str, score: float) -> None:
        if not isinstance(subject, str):
            raise TypeError("Subject must be a string")
        if not isinstance(score, (int, float)):
            raise TypeError("Score must be a number")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        self.grades[subject] = score

    def get_grade(self, subject: str) -> Optional[float]:
        return self.grades.get(subject)

    def get_average(self) -> float:
        if not self.grades:
            return 0.0
        total: float = sum(self.grades.values())
        return total / len(self.grades)

    def get_highest_grade(self) -> Tuple[Optional[str], float]:
        if not self.grades:
            return None, 0
        best_subject: str = max(self.grades, key=self.grades.get)
        return best_subject, self.grades[best_subject]

    def get_lowest_grade(self) -> Tuple[Optional[str], float]:
        if not self.grades:
            return None, 0
        worst_subject: str = min(self.grades, key=self.grades.get)
        return worst_subject, self.grades[worst_subject]

    def get_grade_summary(self) -> str:
        summary: str = f"Grades for {self.name}:\n"
        if not self.grades:
            summary += "  No grades recorded.\n"
            return summary
        for subject in sorted(self.grades.keys()):
            score: float = self.grades[subject]
            letter: str = self._score_to_letter(score)
            bar: str = "#" * int(score / 5)
            summary += f"  {subject:<10}: {score:5.1f} ({letter}) |{bar}|\n"
        summary += f"  Average: {self.get_average():.1f}\n"
        return summary

    def _score_to_letter(self, score: float) -> str:
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def mark_attendance(self, present: bool = True) -> None:
        self.total_classes += 1
        if present:
            self.attendance += 1

    def get_attendance_rate(self) -> float:
        if self.total_classes == 0:
            return 100.0
        return (float(self.attendance) / self.total_classes) * 100

    def to_dict(self) -> Dict[str, object]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grades": dict(self.grades),
            "attendance": self.attendance,
            "total_classes": self.total_classes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> 'Student':
        student: Student = cls(data["student_id"], data["name"], data["age"])
        if "grades" in data:
            for subject, score in data["grades"].items():
                student.grades[subject] = score
        if "attendance" in data:
            student.attendance = data["attendance"]
        if "total_classes" in data:
            student.total_classes = data["total_classes"]
        return student