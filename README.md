# Student Grade Manager - Python 2 Demo Project
--
This is a legacy Python 2 application designed to demonstrate
Python 2 to Python 3 conversion using CodeRenew.
# Python 2 Features Used:
- print statements (not functions)
- raw_input() 
- dict.has_key()
- dict.iteritems() / dict.itervalues()
- old-style exception handling (except Type, e:)
- raise with comma syntax (raise ValueError, "msg")
- basestring / long / unicode types
- reduce() as builtin
- cmp() function and __cmp__ method
- old-style string formatting (% operator)
- Python 2 integer division
- old-style file I/O (open without 'with')
- old-style classes (no object inheritance)

Files:
main.py             - Entry point with interactive menu
student.py          - Student data model
grade_calculator.py - Grade statistics and analysis
data_manager.py     - Data persistence (pickle-based)
report_generator.py - Formatted report output

To run (after converting to Python 3):
> python main.py
