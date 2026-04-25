import pickle
import os
from student import Student
from typing import Dict, List, Optional

class DataManager:
    def __init__(self) -> None:
        self.students: Dict[str, Student] = {}
    
    def add_student(self, student: Student) -> None:
        if student.student_id in self.students:
            print(f"Warning: Student ID {student.student_id} already exists. Updating record.")
        self.students[student.student_id] = student
    
    def remove_student(self, student_id: str) -> bool:
        if student_id in self.students:
            name: str = self.students[student_id].name
            del self.students[student_id]
            print(f"Student '{name}' removed.")
            return True
        else:
            print(f"Student ID {student_id} not found.")
            return False
    
    def find_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)
    
    def get_all_students(self) -> List[Student]:
        return list(self.students.values())
    
    def search(self, query: str) -> List[Student]:
        query: str = query.lower()
        results: List[Student] = []
        
        for student_id, student in self.students.items():
            if query in student.name.lower() or query in student_id.lower():
                results.append(student)
        
        return results
    
    def save_data(self, filename: str) -> bool:
        try:
            data: Dict[str, Dict] = {student_id: student.to_dict() for student_id, student in self.students.items()}
            with open(filename, "wb") as f:
                pickle.dump(data, f)
            print(f"Data saved to {filename} ({len(data)} students)")
            return True
        except IOError as e:
            print(f"Error saving data: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error saving data: {str(e)}")
            return False
    
    def load_data(self, filename: str) -> bool:
        if not os.path.exists(filename):
            print(f"No data file found at {filename}")
            return False
        
        try:
            with open(filename, "rb") as f:
                data: Dict = pickle.load(f)
            self.students = {student_id: Student.from_dict(student_data) for student_id, student_data in data.items()}
            print(f"Loaded {len(self.students)} students from {filename}")
            return True
        except IOError as e:
            print(f"Error loading data: {str(e)}")
            return False
        except Exception as e:
            print(f"Error parsing data file: {str(e)}")
            return False
    
    def get_student_count(self) -> int:
        return len(self.students)
    
    def clear_all(self) -> None:
        count: int = len(self.students)
        self.students.clear()
        print(f"Cleared {count} student records.")