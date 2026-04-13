#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Report Generator - Python 2 style
Generates formatted report cards and statistics reports.
Uses Python 2 string formatting, print statements, and unicode.
"""


class ReportGenerator:
    """Generates formatted reports using Python 2 string operations."""
    
    def generate_report(self, student, calculator):
        """Generate a full report card for a student."""
        report = u""
        report += u"\n" + u"=" * 55 + u"\n"
        report += u"           STUDENT REPORT CARD\n"
        report += u"=" * 55 + u"\n"
        report += u"  Name:       %s\n" % student.name
        report += u"  Student ID: %s\n" % student.student_id
        report += u"  Age:        %d\n" % student.age
        report += u"-" * 55 + u"\n"
        
        if len(student.grades) == 0:
            report += u"  No grades recorded.\n"
            report += u"=" * 55 + u"\n"
            return report
        
        # Grade table header
        report += u"  %-12s  %6s  %5s  %s\n" % ("Subject", "Score", "Grade", "Performance")
        report += u"  " + u"-" * 50 + u"\n"
        
        for subject in sorted(student.grades.keys()):
            score = student.grades[subject]
            letter = self._get_letter_grade(score)
            bar = self._make_bar(score)
            report += u"  %-12s  %6.1f  %5s  %s\n" % (subject, score, letter, bar)
        
        report += u"  " + u"-" * 50 + u"\n"
        
        # Summary
        avg = student.get_average()
        gpa = calculator.calculate_gpa(student)
        best_sub, best_score = student.get_highest_grade()
        worst_sub, worst_score = student.get_lowest_grade()
        
        report += u"\n  SUMMARY\n"
        report += u"  Average Score:  %.1f (%s)\n" % (avg, self._get_letter_grade(avg))
        report += u"  GPA:            %.2f / 4.00\n" % gpa
        report += u"  Best Subject:   %s (%.1f)\n" % (best_sub, best_score)
        report += u"  Weakest:        %s (%.1f)\n" % (worst_sub, worst_score)
        
        # Needs improvement
        weak = calculator.needs_improvement(student)
        if len(weak) > 0:
            report += u"\n  NEEDS IMPROVEMENT:\n"
            for subject, score in weak:
                report += u"    - %s: %.1f (need %.1f more points)\n" % (subject, score, 70 - score)
        
        # Status
        if avg >= 90:
            status = u"EXCELLENT - Honor Roll Candidate"
        elif avg >= 80:
            status = u"GOOD - Keep up the good work"
        elif avg >= 70:
            status = u"SATISFACTORY - Room for improvement"
        elif avg >= 60:
            status = u"NEEDS IMPROVEMENT - At risk"
        else:
            status = u"FAILING - Immediate attention required"
        
        report += u"\n  STATUS: %s\n" % status
        report += u"=" * 55 + u"\n"
        
        return report
    
    def print_statistics(self, stats):
        """Print class statistics in a formatted way."""
        print "\n" + "=" * 55
        print "           CLASS STATISTICS REPORT"
        print "=" * 55
        
        print "\n  OVERVIEW"
        print "  Total Students:        %d" % stats.get("total_students", 0)
        print "  Students with Grades:  %d" % stats.get("students_with_grades", 0)
        
        if stats.has_key("class_average"):
            print "  Class Average:         %.1f" % stats["class_average"]
            print "  Highest Average:       %.1f" % stats["highest_average"]
            print "  Lowest Average:        %.1f" % stats["lowest_average"]
            print "  Std Deviation:         %.2f" % stats["std_deviation"]
        
        if stats.has_key("passing_count"):
            print "\n  PASS / FAIL"
            print "  Passing (>=60%%):       %d" % stats["passing_count"]
            print "  Failing (<60%%):        %d" % stats["failing_count"]
        
        if stats.has_key("grade_distribution"):
            print "\n  GRADE DISTRIBUTION"
            dist = stats["grade_distribution"]
            total = sum(dist.values())
            for grade in ["A", "B", "C", "D", "F"]:
                count = dist.get(grade, 0)
                if total > 0:
                    pct = (count * 100) / total
                else:
                    pct = 0
                bar = "#" * (count * 5)
                print "    %s: %2d (%3d%%) %s" % (grade, count, pct, bar)
        
        if stats.has_key("subjects"):
            print "\n  PER-SUBJECT ANALYSIS"
            for subject, subj_stats in stats["subjects"].iteritems():
                print "    %s:" % subject
                print "      Average: %.1f  |  High: %.1f  |  Low: %.1f" % (
                    subj_stats["average"], subj_stats["highest"], subj_stats["lowest"]
                )
        
        if stats.has_key("top_students"):
            print "\n  TOP PERFORMERS"
            for i, student in enumerate(stats["top_students"]):
                print "    %d. %s (Avg: %.1f)" % (i + 1, student.name, student.get_average())
        
        print "\n" + "=" * 55
    
    def _get_letter_grade(self, score):
        """Convert score to letter grade."""
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
    
    def _make_bar(self, score):
        """Create a visual bar for the score."""
        filled = int(score / 5)
        empty = 20 - filled
        return u"[%s%s]" % (u"#" * filled, u"." * empty)
