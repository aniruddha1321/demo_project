#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Student Grade Manager - A Python 2 Demo Application
====================================================
This application manages student records and grades.
Demonstrates various Python 2 patterns for conversion testing.
"""

from student import Student
from grade_calculator import GradeCalculator
from data_manager import DataManager
from report_generator import ReportGenerator

def show_banner():
    print "=" * 50
    print "   Student Grade Manager v1.0"
    print "   Python 2 Legacy Application"
    print "=" * 50
    print ""

def show_menu():
    print "\n--- Main Menu ---"
    print "1. Add a new student"
    print "2. Record grades"
    print "3. View all students"
    print "4. Generate report card"
    print "5. Class statistics"
    print "6. Search student"
    print "7. Save & Exit"
    print "-" * 20

def add_student(manager):
    print "\n--- Add New Student ---"
    name = raw_input("Enter student name: ")
    age = raw_input("Enter student age: ")
    student_id = raw_input("Enter student ID: ")
    
    try:
        age = int(age)
    except ValueError, e:
        print "Invalid age: %s" % str(e)
        return
    
    student = Student(student_id, name, age)
    manager.add_student(student)
    print "Student '%s' added successfully!" % name

def record_grades(manager):
    print "\n--- Record Grades ---"
    student_id = raw_input("Enter student ID: ")
    student = manager.find_student(student_id)
    
    if student is None:
        print "Student not found!"
        return
    
    print "Recording grades for: %s" % student.name
    subjects = ["Math", "Science", "English", "History", "Art"]
    
    for i in xrange(len(subjects)):
        score = raw_input("Enter %s score (0-100): " % subjects[i])
        try:
            score = float(score)
            if score < 0 or score > 100:
                print "Score must be between 0 and 100"
                continue
            student.add_grade(subjects[i], score)
        except ValueError, e:
            print "Invalid score: %s" % str(e)
    
    print "Grades recorded for %s!" % student.name

def view_students(manager):
    print "\n--- All Students ---"
    students = manager.get_all_students()
    
    if len(students) == 0:
        print "No students registered yet."
        return
    
    for student in students:
        print student
        if student.grades.has_key("Math"):
            print "  Math grade: %.1f" % student.grades["Math"]

def search_student(manager):
    print "\n--- Search Student ---"
    query = raw_input("Enter name or ID to search: ")
    results = manager.search(query)
    
    if len(results) == 0:
        print "No students found matching '%s'" % query
    else:
        print "Found %d student(s):" % len(results)
        for s in results:
            print "  - %s" % unicode(s)

def main():
    show_banner()
    
    manager = DataManager()
    calculator = GradeCalculator()
    reporter = ReportGenerator()
    
    # Load existing data
    loaded = manager.load_data("students.dat")
    if loaded:
        print "Loaded %d existing student records." % len(manager.get_all_students())
    else:
        print "Starting with empty database."
        # Add some sample students for demo
        sample_students = [
            Student("S001", "Alice Johnson", 20),
            Student("S002", "Bob Smith", 21),
            Student("S003", "Charlie Brown", 19),
            Student("S004", "Diana Prince", 22),
        ]
        
        sample_grades = {
            "S001": {"Math": 92, "Science": 88, "English": 95, "History": 87, "Art": 91},
            "S002": {"Math": 78, "Science": 82, "English": 70, "History": 88, "Art": 65},
            "S003": {"Math": 55, "Science": 60, "English": 72, "History": 58, "Art": 80},
            "S004": {"Math": 98, "Science": 95, "English": 92, "History": 96, "Art": 88},
        }
        
        for student in sample_students:
            manager.add_student(student)
            if sample_grades.has_key(student.student_id):
                grades = sample_grades[student.student_id]
                for subject, score in grades.iteritems():
                    student.add_grade(subject, score)
        
        print "Loaded %d sample students for demo." % len(sample_students)
    
    while True:
        show_menu()
        choice = raw_input("Select option (1-7): ")
        
        if choice == "1":
            add_student(manager)
        elif choice == "2":
            record_grades(manager)
        elif choice == "3":
            view_students(manager)
        elif choice == "4":
            student_id = raw_input("Enter student ID for report: ")
            student = manager.find_student(student_id)
            if student:
                report = reporter.generate_report(student, calculator)
                print report
            else:
                print "Student not found!"
        elif choice == "5":
            students = manager.get_all_students()
            if len(students) > 0:
                stats = calculator.class_statistics(students)
                reporter.print_statistics(stats)
            else:
                print "No students to analyze."
        elif choice == "6":
            search_student(manager)
        elif choice == "7":
            manager.save_data("students.dat")
            print "\nData saved. Goodbye!"
            break
        else:
            print "Invalid option. Please try again."

if __name__ == "__main__":
    main()
