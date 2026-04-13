#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Student model class - Python 2 style
Uses old-style classes, print statements, and Python 2 idioms.
"""


class Student:
    """Represents a student with grades - old-style Python 2 class."""
    
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grades = {}
        self.attendance = 0
        self.total_classes = 0
    
    def __str__(self):
        return u"[%s] %s (Age: %d)" % (self.student_id, self.name, self.age)
    
    def __repr__(self):
        return u"Student(%s, %s, %d)" % (self.student_id, self.name, self.age)
    
    def __cmp__(self, other):
        """Compare students by their average grade."""
        avg_self = self.get_average()
        avg_other = other.get_average()
        return cmp(avg_self, avg_other)
    
    def add_grade(self, subject, score):
        """Add or update a grade for a subject."""
        if not isinstance(subject, basestring):
            raise TypeError("Subject must be a string")
        if not isinstance(score, (int, float, long)):
            raise TypeError("Score must be a number")
        if score < 0 or score > 100:
            raise ValueError, "Score must be between 0 and 100"
        self.grades[subject] = score
    
    def get_grade(self, subject):
        """Get grade for a specific subject."""
        if self.grades.has_key(subject):
            return self.grades[subject]
        return None
    
    def get_average(self):
        """Calculate average grade across all subjects."""
        if len(self.grades) == 0:
            return 0.0
        total = reduce(lambda x, y: x + y, self.grades.values())
        return total / len(self.grades)
    
    def get_highest_grade(self):
        """Find the subject with the highest grade."""
        if len(self.grades) == 0:
            return None, 0
        
        best_subject = None
        best_score = -1
        
        for subject, score in self.grades.iteritems():
            if score > best_score:
                best_score = score
                best_subject = subject
        
        return best_subject, best_score
    
    def get_lowest_grade(self):
        """Find the subject with the lowest grade."""
        if len(self.grades) == 0:
            return None, 0
        
        worst_subject = None
        worst_score = 101
        
        for subject, score in self.grades.iteritems():
            if score < worst_score:
                worst_score = score
                worst_subject = subject
        
        return worst_subject, worst_score
    
    def get_grade_summary(self):
        """Get a formatted summary of all grades."""
        summary = u"Grades for %s:\n" % self.name
        if len(self.grades) == 0:
            summary += u"  No grades recorded.\n"
            return summary
        
        for subject in sorted(self.grades.keys()):
            score = self.grades[subject]
            letter = self._score_to_letter(score)
            bar = u"#" * int(score / 5)
            summary += u"  %-10s: %5.1f (%s) |%s|\n" % (subject, score, letter, bar)
        
        summary += u"  Average: %.1f\n" % self.get_average()
        return summary
    
    def _score_to_letter(self, score):
        """Convert numeric score to letter grade."""
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
    
    def mark_attendance(self, present=True):
        """Record attendance for a class."""
        self.total_classes += 1
        if present:
            self.attendance += 1
    
    def get_attendance_rate(self):
        """Get attendance rate as percentage."""
        if self.total_classes == 0:
            return 100.0
        return (float(self.attendance) / self.total_classes) * 100

    def to_dict(self):
        """Convert student to dictionary for serialization."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grades": dict(self.grades.items()),
            "attendance": self.attendance,
            "total_classes": self.total_classes,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Student from a dictionary."""
        student = cls(data["student_id"], data["name"], data["age"])
        if data.has_key("grades"):
            for subject, score in data["grades"].iteritems():
                student.grades[subject] = score
        if data.has_key("attendance"):
            student.attendance = data["attendance"]
        if data.has_key("total_classes"):
            student.total_classes = data["total_classes"]
        return student
