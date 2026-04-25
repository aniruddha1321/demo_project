class Student:
    def __init__(self, name: str, student_id: str, age: int, grades: dict):
        self.name = name
        self.student_id = student_id
        self.age = age
        self.grades = grades

    def get_average(self) -> float:
        if len(self.grades) == 0:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def get_highest_grade(self) -> tuple:
        if len(self.grades) == 0:
            return "", 0.0
        return max(self.grades.items(), key=lambda x: x[1])

    def get_lowest_grade(self) -> tuple:
        if len(self.grades) == 0:
            return "", 0.0
        return min(self.grades.items(), key=lambda x: x[1])


class Calculator:
    def calculate_gpa(self, student: Student) -> float:
        average = student.get_average()
        if average >= 97:
            return 4.33
        elif average >= 93:
            return 4.00
        elif average >= 90:
            return 3.67
        elif average >= 87:
            return 3.33
        elif average >= 83:
            return 3.00
        elif average >= 80:
            return 2.67
        elif average >= 77:
            return 2.33
        elif average >= 73:
            return 2.00
        elif average >= 70:
            return 1.67
        elif average >= 67:
            return 1.33
        elif average >= 63:
            return 1.00
        elif average >= 60:
            return 0.67
        else:
            return 0.00

    def needs_improvement(self, student: Student) -> list:
        weak = []
        for subject, score in student.grades.items():
            if score < 70:
                weak.append((subject, score))
        return weak


class ReportGenerator:
    def generate_report(self, student: Student, calculator: Calculator) -> str:
        report = ""
        report += "\n" + "=" * 55 + "\n"
        report += "           STUDENT REPORT CARD\n"
        report += "=" * 55 + "\n"
        report += f"  Name:       {student.name}\n"
        report += f"  Student ID: {student.student_id}\n"
        report += f"  Age:        {student.age}\n"
        report += "-" * 55 + "\n"

        if len(student.grades) == 0:
            report += "  No grades recorded.\n"
            report += "=" * 55 + "\n"
            return report

        report += "  %-12s  %6s  %5s  %s\n" % ("Subject", "Score", "Grade", "Performance")
        report += "  " + "-" * 50 + "\n"

        for subject in sorted(student.grades.keys()):
            score = student.grades[subject]
            letter = self._get_letter_grade(score)
            bar = self._make_bar(score)
            report += f"  {subject:-12}  {score:6.1f}  {letter:5}  {bar}\n"

        report += "  " + "-" * 50 + "\n"

        avg = student.get_average()
        gpa = calculator.calculate_gpa(student)
        best_sub, best_score = student.get_highest_grade()
        worst_sub, worst_score = student.get_lowest_grade()

        report += "\n  SUMMARY\n"
        report += f"  Average Score:  {avg:.1f} ({self._get_letter_grade(avg)})\n"
        report += f"  GPA:            {gpa:.2f} / 4.00\n"
        report += f"  Best Subject:   {best_sub} ({best_score:.1f})\n"
        report += f"  Weakest:        {worst_sub} ({worst_score:.1f})\n"

        weak = calculator.needs_improvement(student)
        if len(weak) > 0:
            report += "\n  NEEDS IMPROVEMENT:\n"
            for subject, score in weak:
                report += f"    - {subject}: {score:.1f} (need {70 - score:.1f} more points)\n"

        if avg >= 90:
            status = "EXCELLENT - Honor Roll Candidate"
        elif avg >= 80:
            status = "GOOD - Keep up the good work"
        elif avg >= 70:
            status = "SATISFACTORY - Room for improvement"
        elif avg >= 60:
            status = "NEEDS IMPROVEMENT - At risk"
        else:
            status = "FAILING - Immediate attention required"

        report += f"\n  STATUS: {status}\n"
        report += "=" * 55 + "\n"

        return report

    def print_statistics(self, stats: dict) -> None:
        print("\n" + "=" * 55)
        print("           CLASS STATISTICS REPORT")
        print("=" * 55)

        print("\n  OVERVIEW")
        print(f"  Total Students:        {stats.get('total_students', 0)}")
        print(f"  Students with Grades:  {stats.get('students_with_grades', 0)}")

        if "class_average" in stats:
            print(f"  Class Average:         {stats['class_average']:.1f}")
            print(f"  Highest Average:       {stats['highest_average']:.1f}")
            print(f"  Lowest Average:        {stats['lowest_average']:.1f}")
            print(f"  Std Deviation:         {stats['std_deviation']:.2f}")

        if "passing_count" in stats:
            print("\n  PASS / FAIL")
            print(f"  Passing (>=60%%):       {stats['passing_count']}")
            print(f"  Failing (<60%%):        {stats['failing_count']}")

        if "grade_distribution" in stats:
            print("\n  GRADE DISTRIBUTION")
            dist = stats["grade_distribution"]
            total = sum(dist.values())
            for grade in ["A", "B", "C", "D", "F"]:
                count = dist.get(grade, 0)
                if total > 0:
                    pct = (count * 100) / total
                else:
                    pct = 0
                bar = "#" * (count * 5)
                print(f"    {grade}: {count} ({pct:.0f}%) {bar}")

        if "subjects" in stats:
            print("\n  PER-SUBJECT ANALYSIS")
            for subject, subj_stats in stats["subjects"].items():
                print(f"    {subject}:")
                print(f"      Average: {subj_stats['average']:.1f}  |  High: {subj_stats['highest']:.1f}  |  Low: {subj_stats['lowest']:.1f}")

        if "top_students" in stats:
            print("\n  TOP PERFORMERS")
            for i, student in enumerate(stats["top_students"]):
                print(f"    {i + 1}. {student.name} (Avg: {student.get_average():.1f})")

        print("\n" + "=" * 55)

    def _get_letter_grade(self, score: float) -> str:
        if score >= 97:
            return "A+"
        elif score >= 93:
            return "A"
        elif score >= 90:
            return "A-"
        elif score >= 87:
            return "B+"
        elif score >= 83:
            return "B"
        elif score >= 80:
            return "B-"
        elif score >= 77:
            return "C+"
        elif score >= 73:
            return "C"
        elif score >= 70:
            return "C-"
        elif score >= 67:
            return "D+"
        elif score >= 63:
            return "D"
        elif score >= 60:
            return "D-"
        else:
            return "F"

    def _make_bar(self, score: float) -> str:
        filled = int(score / 5)
        empty = 20 - filled
        return f"[{'#' * filled}{'.' * empty}]"