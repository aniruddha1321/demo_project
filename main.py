from student import Student
from grade_calculator import GradeCalculator
from data_manager import DataManager
from report_generator import ReportGenerator

def show_banner() -> None:
    print("=" * 50)
    print("   Student Grade Manager v1.0")
    print("   Python 3 Application")
    print("=" * 50)
    print("")

def show_menu() -> None:
    print("\n--- Main Menu ---")
    print("1. Add a new student")
    print("2. Record grades")
    print("3. View all students")
    print("4. Generate report card")
    print("5. Class statistics")
    print("6. Search student")
    print("7. Save & Exit")
    print("-" * 20)

def add_student(manager: DataManager) -> None:
    print("\n--- Add New Student ---")
    name: str = input("Enter student name: ")
    age: str = input("Enter student age: ")
    student_id: str = input("Enter student ID: ")
    
    try:
        age: int = int(age)
    except ValueError as e:
        print(f"Invalid age: {e}")
        return
    
    student: Student = Student(student_id, name, age)
    manager.add_student(student)
    print(f"Student '{name}' added successfully!")

def record_grades(manager: DataManager) -> None:
    print("\n--- Record Grades ---")
    student_id: str = input("Enter student ID: ")
    student: Student | None = manager.find_student(student_id)
    
    if student is None:
        print("Student not found!")
        return
    
    print(f"Recording grades for: {student.name}")
    subjects: list[str] = ["Math", "Science", "English", "History", "Art"]
    
    for subject in subjects:
        while True:
            try:
                score: float = float(input(f"Enter {subject} score (0-100): "))
                if 0 <= score <= 100:
                    student.add_grade(subject, score)
                    break
                else:
                    print("Score must be between 0 and 100")
            except ValueError as e:
                print(f"Invalid score: {e}")
    
    print(f"Grades recorded for {student.name}!")

def view_students(manager: DataManager) -> None:
    print("\n--- All Students ---")
    students: list[Student] = manager.get_all_students()
    
    if not students:
        print("No students registered yet.")
        return
    
    for student in students:
        print(student)
        if "Math" in student.grades:
            print(f"  Math grade: {student.grades['Math']:.1f}")

def search_student(manager: DataManager) -> None:
    print("\n--- Search Student ---")
    query: str = input("Enter name or ID to search: ")
    results: list[Student] = manager.search(query)
    
    if not results:
        print(f"No students found matching '{query}'")
    else:
        print(f"Found {len(results)} student(s):")
        for student in results:
            print(f"  - {student}")

def main() -> None:
    show_banner()
    
    manager: DataManager = DataManager()
    calculator: GradeCalculator = GradeCalculator()
    reporter: ReportGenerator = ReportGenerator()
    
    loaded: bool = manager.load_data("students.dat")
    if loaded:
        print(f"Loaded {len(manager.get_all_students())} existing student records.")
    else:
        print("Starting with empty database.")
        sample_students: list[Student] = [
            Student("S001", "Alice Johnson", 20),
            Student("S002", "Bob Smith", 21),
            Student("S003", "Charlie Brown", 19),
            Student("S004", "Diana Prince", 22),
        ]
        
        sample_grades: dict[str, dict[str, int]] = {
            "S001": {"Math": 92, "Science": 88, "English": 95, "History": 87, "Art": 91},
            "S002": {"Math": 78, "Science": 82, "English": 70, "History": 88, "Art": 65},
            "S003": {"Math": 55, "Science": 60, "English": 72, "History": 58, "Art": 80},
            "S004": {"Math": 98, "Science": 95, "English": 92, "History": 96, "Art": 88},
        }
        
        for student in sample_students:
            manager.add_student(student)
            if student.student_id in sample_grades:
                grades: dict[str, int] = sample_grades[student.student_id]
                for subject, score in grades.items():
                    student.add_grade(subject, score)
        
        print(f"Loaded {len(sample_students)} sample students for demo.")
    
    while True:
        show_menu()
        choice: str = input("Select option (1-7): ")
        
        if choice == "1":
            add_student(manager)
        elif choice == "2":
            record_grades(manager)
        elif choice == "3":
            view_students(manager)
        elif choice == "4":
            student_id: str = input("Enter student ID for report: ")
            student: Student | None = manager.find_student(student_id)
            if student:
                report: str = reporter.generate_report(student, calculator)
                print(report)
            else:
                print("Student not found!")
        elif choice == "5":
            students: list[Student] = manager.get_all_students()
            if students:
                stats: dict[str, float] = calculator.class_statistics(students)
                reporter.print_statistics(stats)
            else:
                print("No students to analyze.")
        elif choice == "6":
            search_student(manager)
        elif choice == "7":
            manager.save_data("students.dat")
            print("\nData saved. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()