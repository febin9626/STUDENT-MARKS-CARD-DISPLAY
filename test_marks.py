import unittest
from student_marks_card import (
    Student,
    Subject,
    get_subject_grade,
    calculate_cgpa,
    get_division,
    get_student_summary,
    load_all_students,
    find_student
)


class TestStudentMarks(unittest.TestCase):
    def setUp(self):
        self.sub_math = Subject("MTH101", "Mathematics", 95, 100, 40)
        self.sub_phy = Subject("PHY102", "Physics", 85, 100, 40)
        self.sub_chem = Subject("CHM103", "Chemistry", 75, 100, 40)

    def test_pass_status_and_percentage(self):
        self.assertTrue(self.sub_math.is_pass)
        self.assertEqual(self.sub_math.percentage, 95.0)

        failing = Subject("BIO104", "Biology", 32, 100, 40)
        self.assertFalse(failing.is_pass)

    def test_subject_validation(self):
        # Marks cannot exceed maximum marks
        with self.assertRaises(ValueError):
            Subject("TST", "Invalid", 105, 100, 40)

        # Marks cannot be negative
        with self.assertRaises(ValueError):
            Subject("TST", "Invalid", -5, 100, 40)

    def test_student_totals(self):
        student = Student("101", "Arjun Patel", "Class 10")
        student.add_subject(self.sub_math)
        student.add_subject(self.sub_phy)
        student.add_subject(self.sub_chem)

        self.assertEqual(student.total_obtained, 255.0)
        self.assertEqual(student.total_max, 300.0)
        self.assertEqual(student.percentage, 85.0)
        self.assertTrue(student.has_passed_all)

    def test_distinction_division(self):
        student = Student("101", "Arjun Patel", "Class 10")
        student.add_subject(self.sub_math)
        student.add_subject(self.sub_phy)
        student.add_subject(self.sub_chem)

        summary = get_student_summary(student)
        self.assertEqual(summary["status"], "PASS")
        self.assertEqual(summary["division"], "First Class with Distinction")
        self.assertEqual(summary["cgpa"], 9.0)

    def test_failed_subject_flag(self):
        student = Student("103", "Rohan Joseph", "Class 10")
        student.add_subject(self.sub_math)
        failed_sub = Subject("PHY102", "Physics", 32, 100, 40)
        student.add_subject(failed_sub)

        self.assertFalse(student.has_passed_all)
        self.assertEqual(len(student.failed_subjects), 1)

        summary = get_student_summary(student)
        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["division"], "Fail")

    def test_find_student(self):
        found = find_student("101")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Arjun Patel")


if __name__ == "__main__":
    unittest.main()
