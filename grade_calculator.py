#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grade Calculator - Python 2 style
Performs statistical analysis on student grades.
Uses Python 2 division, xrange, map/filter, and print statements.
"""

import math


class GradeCalculator:
    """Calculates grade statistics using Python 2 idioms."""
    
    # Grade boundaries
    GRADE_BOUNDARIES = {
        "A+": 97, "A": 93, "A-": 90,
        "B+": 87, "B": 83, "B-": 80,
        "C+": 77, "C": 73, "C-": 70,
        "D+": 67, "D": 63, "D-": 60,
        "F": 0
    }
    
    def calculate_gpa(self, student):
        """Calculate GPA on a 4.0 scale."""
        if len(student.grades) == 0:
            return 0.0
        
        total_points = 0
        for subject, score in student.grades.iteritems():
            if score >= 90:
                points = 4.0
            elif score >= 80:
                points = 3.0
            elif score >= 70:
                points = 2.0
            elif score >= 60:
                points = 1.0
            else:
                points = 0.0
            total_points += points
        
        # Python 2 integer division issue - intentionally using old style
        gpa = total_points / len(student.grades)
        return round(gpa, 2)
    
    def calculate_percentile(self, student, all_students):
        """Calculate student's percentile rank in classs."""
        if len(all_students) <= 1:
            return 100.0
        
        student_avg = student.get_average()
        below_count = 0
        
        for s in all_students:
            if s.student_id != student.student_id:
                if s.get_average() < student_avg:
                    below_count += 1
        
        # Python 2 division
        percentile = (below_count * 100) / (len(all_students) - 1)
        return round(float(percentile), 1)
    
    def curved_score(self, score, class_avg, target_avg=75):
        """Apply curve to a score based on class average."""
        if class_avg == 0:
            return score
        adjustment = target_avg - class_avg
        curved = score + adjustment
        # Clamp between 0 and 100
        return max(0, min(100, curved))
    
    def class_statistics(self, students):
        """Calculate comprehensive class statistics."""
        if len(students) == 0:
            return {}
        
        all_averages = []
        subject_scores = {}
        
        for student in students:
            avg = student.get_average()
            if avg > 0:
                all_averages.append(avg)
            
            for subject, score in student.grades.iteritems():
                if not subject_scores.has_key(subject):
                    subject_scores[subject] = []
                subject_scores[subject].append(score)
        
        stats = {
            "total_students": len(students),
            "students_with_grades": len(filter(lambda s: len(s.grades) > 0, students)),
        }
        
        if len(all_averages) > 0:
            stats["class_average"] = sum(all_averages) / len(all_averages)
            stats["highest_average"] = max(all_averages)
            stats["lowest_average"] = min(all_averages)
            
            # Calculate standard deviation
            mean = stats["class_average"]
            variance = sum(map(lambda x: (x - mean) ** 2, all_averages)) / len(all_averages)
            stats["std_deviation"] = math.sqrt(variance)
            
            # Grade distribution
            grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
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
        
        # Per-subject statistics
        subject_stats = {}
        for subject, scores in subject_scores.iteritems():
            subject_stats[subject] = {
                "average": sum(scores) / len(scores),
                "highest": max(scores),
                "lowest": min(scores),
                "count": len(scores),
            }
        stats["subjects"] = subject_stats
        
        # Find top performers
        sorted_students = sorted(students, key=lambda s: s.get_average(), reverse=True)
        stats["top_students"] = sorted_students[:3]
        
        # Pass/fail count (60% threshold)
        passing = filter(lambda s: s.get_average() >= 60, students)
        stats["passing_count"] = len(list(passing))
        stats["failing_count"] = len(students) - stats["passing_count"]
        
        return stats
    
    def needs_improvement(self, student, threshold=70):
        """List subjects where student needs improvement."""
        weak_subjects = []
        for subject, score in student.grades.iteritems():
            if score < threshold:
                weak_subjects.append((subject, score))
        
        # Sort by score ascending
        weak_subjects.sort(key=lambda x: x[1])
        return weak_subjects
    
    def honor_roll(self, students, min_gpa=3.5):
        """Get students qualifying for honor roll."""
        eligible = []
        for student in students:
            gpa = self.calculate_gpa(student)
            if gpa >= min_gpa:
                eligible.append((student, gpa))
        
        # Sort by GPA descending
        eligible.sort(key=lambda x: x[1], reverse=True)
        return eligible
