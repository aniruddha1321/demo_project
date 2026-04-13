#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Manager - Python 2 style
Handles loading and saving student data.
Uses old-style exception handling, file I/O, and pickle.
"""

import pickle
import os


class DataManager:
    """Manages student data persistence using Python 2 patterns."""
    
    def __init__(self):
        self.students = {}  # student_id -> Student
    
    def add_student(self, student):
        """Add a student to the database."""
        if self.students.has_key(student.student_id):
            print "Warning: Student ID %s already exists. Updating record." % student.student_id
        self.students[student.student_id] = student
    
    def remove_student(self, student_id):
        """Remove a student from the database."""
        if self.students.has_key(student_id):
            name = self.students[student_id].name
            del self.students[student_id]
            print "Student '%s' removed." % name
            return True
        else:
            print "Student ID %s not found." % student_id
            return False
    
    def find_student(self, student_id):
        """Find a student by ID."""
        if self.students.has_key(student_id):
            return self.students[student_id]
        return None
    
    def get_all_students(self):
        """Get all students as a list."""
        return self.students.values()
    
    def search(self, query):
        """Search students by name or ID."""
        query = query.lower()
        results = []
        
        for student_id, student in self.students.iteritems():
            if query in student.name.lower() or query in student_id.lower():
                results.append(student)
        
        return results
    
    def save_data(self, filename):
        """Save all student data to a file."""
        try:
            data = {}
            for student_id, student in self.students.iteritems():
                data[student_id] = student.to_dict()
            
            f = open(filename, "wb")
            try:
                pickle.dump(data, f)
                print "Data saved to %s (%d students)" % (filename, len(data))
            finally:
                f.close()
            
            return True
        except IOError, e:
            print "Error saving data: %s" % str(e)
            return False
        except Exception, e:
            print "Unexpected error saving data: %s" % str(e)
            return False
    
    def load_data(self, filename):
        """Load student data from a file."""
        if not os.path.exists(filename):
            print "No data file found at %s" % filename
            return False
        
        try:
            f = open(filename, "rb")
            try:
                data = pickle.load(f)
            finally:
                f.close()
            
            from student import Student
            self.students = {}
            for student_id, student_data in data.iteritems():
                self.students[student_id] = Student.from_dict(student_data)
            
            print "Loaded %d students from %s" % (len(self.students), filename)
            return True
        except IOError, e:
            print "Error loading data: %s" % str(e)
            return False
        except Exception, e:
            print "Error parsing data file: %s" % str(e)
            return False
    
    def get_student_count(self):
        """Get total number of students."""
        return len(self.students)
    
    def clear_all(self):
        """Remove all students."""
        count = len(self.students)
        self.students.clear()
        print "Cleared %d student records." % count
