import math
from typing import Dict, List, Tuple

class Student:
    def __init__(self, student_id: int, grades: Dict[str, float]):
        self.student_id = student_id
        self.grades = grades

    def get_average(self) -> float:
        if len(self.grades) == 0:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)


class GradeCalculator:
    GRADE_BOUNDARIES: Dict[str, int] = {
        "A+": 97, "A": 93, "A-": 90,
        "B+": 87, "B": 83, "B-": 80,
        "C+": 77, "C": 73, "C-": 70,
        "D+": 67, "D": 63, "D-": 60,
        "F": 0
    }

    def calculate_gpa(self, student: Student) -> float:
        if len(student.grades) == 0:
            return 0.0
        
        total_points: float = 0
        for score in student.grades.values():
            if score >= 90:
                points: float = 4.0
            elif score >= 80:
                points = 3.0
            elif score >= 70:
                points = 2.0
            elif score >= 60:
                points = 1.0
            else:
                points = 0.0
            total_points += points
        
        gpa: float = total_points / len(student.grades)
        return round(gpa, 2)
    
    def calculate_percentile(self, student: Student, all_students: List[Student]) -> float:
        if len(all_students) <= 1:
            return 100.0
        
        student_avg: float = student.get_average()
        below_count: int = 0
        
        for s in all_students:
            if s.student_id != student.student_id:
                if s.get_average() < student_avg:
                    below_count += 1
        
        percentile: float = (below_count * 100) / (len(all_students) - 1)
        return round(percentile, 1)
    
    def curved_score(self, score: float, class_avg: float, target_avg: float = 75) -> float:
        if class_avg == 0:
            return score
        adjustment: float = target_avg - class_avg
        curved: float = score + adjustment
        return max(0, min(100, curved))
    
    def class_statistics(self, students: List[Student]) -> Dict[str, float]:
        if len(students) == 0:
            return {}
        
        all_averages: List[float] = []
        subject_scores: Dict[str, List[float]] = {}
        
        for student in students:
            avg: float = student.get_average()
            if avg > 0:
                all_averages.append(avg)
            
            for subject, score in student.grades.items():
                if subject not in subject_scores:
                    subject_scores[subject] = []
                subject_scores[subject].append(score)
        
        stats: Dict[str, float] = {
            "total_students": len(students),
            "students_with_grades": len([s for s in students if len(s.grades) > 0]),
        }
        
        if len(all_averages) > 0:
            stats["class_average"] = sum(all_averages) / len(all_averages)
            stats["highest_average"] = max(all_averages)
            stats["lowest_average"] = min(all_averages)
            
            mean: float = stats["class_average"]
            variance: float = sum([(x - mean) ** 2 for x in all_averages]) / len(all_averages)
            stats["std_deviation"] = math.sqrt(variance)
            
            grade_dist: Dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
            for avg in all_averages:
                if avg >= 90:
                    grade_dist["A"] += 1
                elif avg >= 80:
                    grade_dist["B"] += 1
                elif avg >= 70:
                    grade_dist["C"] += 1
                elif avg >= 60:
                    grade_dist["D"] += 1
                else:
                    grade_dist["F"] += 1
            stats["grade_distribution"] = grade_dist
        
        subject_stats: Dict[str, Dict[str, float]] = {}
        for subject, scores in subject_scores.items():
            subject_stats[subject] = {
                "average": sum(scores) / len(scores),
                "highest": max(scores),
                "lowest": min(scores),
                "count": len(scores),
            }
        stats["subjects"] = subject_stats
        
        sorted_students: List[Student] = sorted(students, key=lambda s: s.get_average(), reverse=True)
        stats["top_students"] = sorted_students[:3]
        
        passing: List[Student] = [s for s in students if s.get_average() >= 60]
        stats["passing_count"] = len(passing)
        stats["failing_count"] = len(students) - stats["passing_count"]
        
        return stats
    
    def needs_improvement(self, student: Student, threshold: float = 70) -> List[Tuple[str, float]]:
        weak_subjects: List[Tuple[str, float]] = []
        for subject, score in student.grades.items():
            if score < threshold:
                weak_subjects.append((subject, score))
        
        weak_subjects.sort(key=lambda x: x[1])
        return weak_subjects
    
    def honor_roll(self, students: List[Student], min_gpa: float = 3.5) -> List[Tuple[Student, float]]:
        eligible: List[Tuple[Student, float]] = []
        for student in students:
            gpa: float = self.calculate_gpa(student)
            if gpa >= min_gpa:
                eligible.append((student, gpa))
        
        eligible.sort(key=lambda x: x[1], reverse=True)
        return eligible