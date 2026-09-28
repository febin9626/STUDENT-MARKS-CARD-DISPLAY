"""
STUDENT MARKS CARD & PERFORMANCE REPORT SYSTEM
"""

import sys
import os
import unittest
from datetime import datetime


# ==============================================================================
# 1. CORE DATA MODELS (Subject and Student)
# ==============================================================================

class Subject:
    def __init__(self, code, name, marks, max_marks=100.0, pass_marks=40.0):
        self.code = str(code).strip().upper()
        self.name = str(name).strip()
        self.marks = float(marks)
        self.max_marks = float(max_marks)
        self.pass_marks = float(pass_marks)

        # Validation
        if self.max_marks <= 0:
            raise ValueError(f"Max marks for {self.name} must be greater than 0")
        if self.marks < 0:
            raise ValueError(f"Marks for {self.name} cannot be negative")
        if self.marks > self.max_marks:
            raise ValueError(f"Marks ({self.marks}) cannot exceed max marks ({self.max_marks})")

    @property
    def percentage(self):
        return round((self.marks / self.max_marks) * 100, 2)

    @property
    def is_pass(self):
        return self.marks >= self.pass_marks

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "marks": self.marks,
            "max_marks": self.max_marks,
            "pass_marks": self.pass_marks
        }


class Student:
    def __init__(self, roll_no, name, student_class="Class 10", school="St. Xavier's High School", academic_year="2025-2026"):
        self.roll_no = str(roll_no).strip()
        self.name = str(name).strip()
        self.student_class = str(student_class).strip()
        self.school = str(school).strip()
        self.academic_year = str(academic_year).strip()
        self.subjects = []

    def add_subject(self, subject):
        self.subjects.append(subject)

    @property
    def total_obtained(self):
        return sum(s.marks for s in self.subjects)

    @property
    def total_max(self):
        return sum(s.max_marks for s in self.subjects)

    @property
    def percentage(self):
        if self.total_max == 0:
            return 0.0
        return round((self.total_obtained / self.total_max) * 100, 2)

    @property
    def has_passed_all(self):
        return len(self.subjects) > 0 and all(s.is_pass for s in self.subjects)

    @property
    def failed_subjects(self):
        return [s for s in self.subjects if not s.is_pass]

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "class": self.student_class,
            "school": self.school,
            "academic_year": self.academic_year,
            "subjects": [s.to_dict() for s in self.subjects]
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(
            roll_no=data["roll_no"],
            name=data["name"],
            student_class=data.get("class", "Class 10"),
            school=data.get("school", "St. Xavier's High School"),
            academic_year=data.get("academic_year", "2025-2026")
        )
        for s_data in data.get("subjects", []):
            subj = Subject(
                code=s_data["code"],
                name=s_data["name"],
                marks=s_data["marks"],
                max_marks=s_data.get("max_marks", 100.0),
                pass_marks=s_data.get("pass_marks", 40.0)
            )
            student.add_subject(subj)
        return student


# ==============================================================================
# 2. GRADING & EVALUATION FUNCTIONS
# ==============================================================================

def get_subject_grade(marks, max_marks=100.0, pass_marks=40.0):
    """Calculates letter grade, grade points (10-point scale), and performance remark."""
    if marks < pass_marks:
        return "F", 0.0, "Fail"

    pct = (marks / max_marks) * 100.0 if max_marks > 0 else 0.0
    if pct >= 90.0:
        return "A+", 10.0, "Outstanding"
    elif pct >= 80.0:
        return "A", 9.0, "Excellent"
    elif pct >= 70.0:
        return "B+", 8.0, "Very Good"
    elif pct >= 60.0:
        return "B", 7.0, "Good"
    elif pct >= 50.0:
        return "C", 6.0, "Average"
    elif pct >= 40.0:
        return "D", 5.0, "Satisfactory"
    return "F", 0.0, "Fail"


def calculate_cgpa(student):
    """Calculates overall CGPA out of 10.0."""
    if not student.subjects:
        return 0.0

    points = []
    for s in student.subjects:
        _, gp, _ = get_subject_grade(s.marks, s.max_marks, s.pass_marks)
        points.append(gp)

    return round(sum(points) / len(points), 2)


def get_division(percentage, passed_all):
    """Determines student academic division / honor."""
    if not passed_all:
        return "Fail"

    if percentage >= 75.0:
        return "First Class with Distinction"
    elif percentage >= 60.0:
        return "First Class"
    elif percentage >= 50.0:
        return "Second Class"
    elif percentage >= 40.0:
        return "Pass Class"
    return "Fail"


def get_student_summary(student):
    """Compiles overall totals, percentage, CGPA, grade, and status."""
    passed_all = student.has_passed_all
    pct = student.percentage
    cgpa = calculate_cgpa(student)
    division = get_division(pct, passed_all)

    if passed_all:
        if pct >= 90.0:
            overall_grade = "A+"
        elif pct >= 80.0:
            overall_grade = "A"
        elif pct >= 70.0:
            overall_grade = "B+"
        elif pct >= 60.0:
            overall_grade = "B"
        elif pct >= 50.0:
            overall_grade = "C"
        else:
            overall_grade = "D"
    else:
        overall_grade = "F"

    return {
        "total_obtained": student.total_obtained,
        "total_max": student.total_max,
        "percentage": pct,
        "cgpa": cgpa,
        "status": "PASS" if passed_all else "FAIL",
        "overall_grade": overall_grade,
        "division": division,
        "failed_count": len(student.failed_subjects)
    }


# ==============================================================================
# 3. SAMPLE DATA (Stored directly in Python)
# ==============================================================================

DEFAULT_STUDENT_RECORDS = [
    {
        "roll_no": "101",
        "name": "Arjun Patel",
        "class": "Class 10 - Section A",
        "school": "St. Xavier's High School",
        "academic_year": "2025-2026",
        "subjects": [
            {"code": "ENG101", "name": "English", "marks": 88.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "MTH102", "name": "Mathematics", "marks": 95.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "PHY103", "name": "Physics", "marks": 92.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "CHM104", "name": "Chemistry", "marks": 85.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "CS105",  "name": "Computer Science", "marks": 98.0, "max_marks": 100.0, "pass_marks": 40.0}
        ]
    },
    {
        "roll_no": "102",
        "name": "Priya Sharma",
        "class": "Class 10 - Section A",
        "school": "St. Xavier's High School",
        "academic_year": "2025-2026",
        "subjects": [
            {"code": "ENG101", "name": "English", "marks": 78.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "MTH102", "name": "Mathematics", "marks": 72.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "PHY103", "name": "Physics", "marks": 65.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "CHM104", "name": "Chemistry", "marks": 70.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "CS105",  "name": "Computer Science", "marks": 82.0, "max_marks": 100.0, "pass_marks": 40.0}
        ]
    },
    {
        "roll_no": "103",
        "name": "Rohan Joseph",
        "class": "Class 10 - Section B",
        "school": "St. Xavier's High School",
        "academic_year": "2025-2026",
        "subjects": [
            {"code": "ENG101", "name": "English", "marks": 54.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "MTH102", "name": "Mathematics", "marks": 48.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "PHY103", "name": "Physics", "marks": 32.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "CHM104", "name": "Chemistry", "marks": 42.0, "max_marks": 100.0, "pass_marks": 40.0},
            {"code": "CS105",  "name": "Computer Science", "marks": 58.0, "max_marks": 100.0, "pass_marks": 40.0}
        ]
    }
]


# ==============================================================================
# 4. PURE PYTHON STORAGE (No external JSON or database)
# ==============================================================================

DATA_FILE_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students_data.py")


def load_all_students():
    """Loads student records from students_data.py or falls back to DEFAULT_STUDENT_RECORDS."""
    if os.path.exists(DATA_FILE_PY):
        try:
            scope = {}
            with open(DATA_FILE_PY, "r", encoding="utf-8") as f:
                code_text = f.read()
            exec(code_text, scope)
            records = scope.get("STUDENTS", DEFAULT_STUDENT_RECORDS)
            return [Student.from_dict(r) for r in records]
        except Exception:
            pass

    return [Student.from_dict(r) for r in DEFAULT_STUDENT_RECORDS]


def save_all_students(students):
    """Saves student records directly into students_data.py as pure Python code."""
    records = [s.to_dict() for s in students]
    lines = [
        "# Auto-generated student database (Pure Python)",
        f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "STUDENTS = ["
    ]
    for r in records:
        lines.append("    {")
        lines.append(f"        'roll_no': {repr(r['roll_no'])},")
        lines.append(f"        'name': {repr(r['name'])},")
        lines.append(f"        'class': {repr(r['class'])},")
        lines.append(f"        'school': {repr(r['school'])},")
        lines.append(f"        'academic_year': {repr(r['academic_year'])},")
        lines.append("        'subjects': [")
        for sub in r["subjects"]:
            lines.append(f"            {repr(sub)},")
        lines.append("        ]")
        lines.append("    },")
    lines.append("]")
    lines.append("")

    with open(DATA_FILE_PY, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def find_student(roll_no):
    target = str(roll_no).strip().lower()
    for s in load_all_students():
        if s.roll_no.lower() == target:
            return s
    return None


# ==============================================================================
# 5. MARKS CARD FORMATTING & DISPLAY
# ==============================================================================

# Terminal color constants
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"


def format_marks_card(student, use_color=False):
    summary = get_student_summary(student)
    card_width = 87
    content_width = card_width - 4  # exactly 83 characters between '| ' and ' |'

    def border(char="-"):
        return "+" + (char * (card_width - 2)) + "+"

    def row(text, align="left"):
        t = text[:content_width]
        if align == "center":
            return f"| {t.center(content_width)} |"
        elif align == "right":
            return f"| {t.rjust(content_width)} |"
        return f"| {t.ljust(content_width)} |"

    def two_col(left_str, right_str):
        l_width = 41
        r_width = 42
        l = left_str[:l_width].ljust(l_width)
        r = right_str[:r_width].ljust(r_width)
        return f"| {l}{r} |"

    lines = []

    # School & Report Header
    lines.append(border("="))
    lines.append(row(student.school.upper(), "center"))
    lines.append(row("STUDENT PROGRESS REPORT & MARKS CARD", "center"))
    lines.append(row(f"Academic Year: {student.academic_year}", "center"))
    lines.append(border("="))

    # Student Details
    lines.append(two_col(f"Student Name : {student.name}", f"Roll Number : {student.roll_no}"))
    lines.append(two_col(f"Class/Course : {student.student_class}", f"Date Issued : {datetime.now().strftime('%d-%b-%Y')}"))
    lines.append(border("-"))

    # Table Header (Exact 87 characters)
    hdr = "| CODE     | SUBJECT NAME             |   MAX |  PASS |  OBT  | GRADE |  GP  | STATUS |"
    lines.append(hdr)
    lines.append("+----------+--------------------------+-------+-------+-------+-------+------+--------+")

    # Table Rows
    for sub in student.subjects:
        grade, gp, _ = get_subject_grade(sub.marks, sub.max_marks, sub.pass_marks)
        st = "PASS" if sub.is_pass else "FAIL"

        r = (
            f"| {sub.code:<8} | {sub.name[:24]:<24} | {sub.max_marks:>5.1f} | "
            f"{sub.pass_marks:>5.1f} | {sub.marks:>5.1f} | {grade:^5} | {gp:>4.1f} | {st:^6} |"
        )
        lines.append(r)

    lines.append("+----------+--------------------------+-------+-------+-------+-------+------+--------+")

    # Summary
    t_obtained = f"Total Marks : {summary['total_obtained']:.1f} / {summary['total_max']:.1f}"
    pct_text = f"Percentage  : {summary['percentage']:.2f}%"
    lines.append(two_col(t_obtained, pct_text))

    cgpa_text = f"CGPA        : {summary['cgpa']:.2f} / 10.0"
    res_text = f"Final Result: {summary['status']}"
    lines.append(two_col(cgpa_text, res_text))

    grade_text = f"Grade       : {summary['overall_grade']}"
    div_text = f"Division    : {summary['division']}"
    lines.append(two_col(grade_text, div_text))

    lines.append(border("-"))

    # Remarks
    if summary["failed_count"] > 0:
        lines.append(row(f"Remarks: Supplementary exam required in {summary['failed_count']} subject(s)."))
    else:
        lines.append(row("Remarks: Congratulations! Promoted to the next academic level."))

    lines.append(border("-"))

    # Signatures
    lines.append(row(""))
    sig_line = f"{'_________________________':<41}{'_________________________':>42}"
    lines.append(row(sig_line))
    sig_names = f"{'Class Teacher':<41}{'Principal':>42}"
    lines.append(row(sig_names))
    lines.append(border("="))

    text_card = "\n".join(lines)

    if not use_color:
        return text_card

    colored_lines = []
    for line in text_card.split("\n"):
        if "STUDENT PROGRESS REPORT" in line or student.school.upper() in line:
            line = f"{BOLD}{CYAN}{line}{RESET}"
        elif "| PASS |" in line:
            line = line.replace("PASS", f"{GREEN}PASS{RESET}")
        elif "| FAIL |" in line:
            line = line.replace("FAIL", f"{RED}FAIL{RESET}")

        if "Final Result: PASS" in line:
            line = line.replace("PASS", f"{BOLD}{GREEN}PASS{RESET}")
        elif "Final Result: FAIL" in line:
            line = line.replace("FAIL", f"{BOLD}{RED}FAIL{RESET}")

        if "Distinction" in line:
            line = line.replace("Distinction", f"{YELLOW}Distinction{RESET}")

        colored_lines.append(line)

    return "\n".join(colored_lines)


def print_marks_card(student):
    print(format_marks_card(student, use_color=True))


# ==============================================================================
# 6. INTERACTIVE MENU ACTIONS
# ==============================================================================

def show_menu():
    print("\n" + "=" * 45)
    print("      STUDENT MARKS CARD SYSTEM")
    print("=" * 45)
    print("1. View Sample Marks Card (Quick Demo)")
    print("2. Search Student by Roll Number")
    print("3. View All Students Summary List")
    print("4. Add New Student and Marks")
    print("5. Run Built-in Unit Tests")
    print("6. Exit")
    print("-" * 45)


def add_student_interactive():
    print("\n--- Enter Student Details ---")
    roll = input("Roll Number: ").strip()
    if not roll:
        print("Roll number cannot be empty.")
        return

    existing = find_student(roll)
    if existing:
        ans = input(f"Student with roll {roll} exists ({existing.name}). Overwrite? (y/n): ").lower()
        if ans != "y":
            return

    name = input("Student Full Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    student_class = input("Class / Section (default: Class 10): ").strip() or "Class 10"
    school = input("School Name (default: St. Xavier's High School): ").strip() or "St. Xavier's High School"

    student = Student(roll_no=roll, name=name, student_class=student_class, school=school)

    print("\nEnter subjects (press Enter on empty name when finished):")
    idx = 1
    while True:
        sub_name = input(f"\nSubject #{idx} Name: ").strip()
        if not sub_name:
            if idx == 1:
                print("Please enter at least one subject.")
                continue
            break

        code = input(f"Subject Code (default: SUB{idx:02d}): ").strip() or f"SUB{idx:02d}"

        try:
            max_m = float(input("Max Marks (default: 100): ").strip() or "100")
            pass_m = float(input("Passing Marks (default: 40): ").strip() or "40")
            marks = float(input(f"Marks Obtained (0 to {max_m}): ").strip())

            sub = Subject(code=code, name=sub_name, marks=marks, max_marks=max_m, pass_marks=pass_m)
            student.add_subject(sub)
            idx += 1
        except ValueError as err:
            print(f"Invalid input: {err}. Please re-enter this subject.")

    all_students = load_all_students()
    all_students = [s for s in all_students if s.roll_no.lower() != roll.lower()]
    all_students.append(student)
    save_all_students(all_students)

    print(f"\n{GREEN}Student saved successfully!{RESET}\n")
    print_marks_card(student)


def list_all_students():
    students = load_all_students()
    if not students:
        print("No student records found.")
        return

    print(f"\n{'ROLL':<8} {'NAME':<20} {'CLASS':<16} {'TOTAL':<12} {'%':<8} {'CGPA':<6} {'STATUS'}")
    print("-" * 78)

    for s in students:
        info = get_student_summary(s)
        total_str = f"{info['total_obtained']:.0f}/{info['total_max']:.0f}"
        badge = f"{GREEN}PASS{RESET}" if info["status"] == "PASS" else f"{RED}FAIL{RESET}"

        print(
            f"{s.roll_no:<8} {s.name[:18]:<20} {s.student_class[:14]:<16} "
            f"{total_str:<12} {info['percentage']:>6.1f}% {info['cgpa']:>5.2f}  {badge}"
        )
    print("-" * 78)


# ==============================================================================
# 7. BUILT-IN UNIT TESTS (Executable directly with --test)
# ==============================================================================

class BuiltinMarksTests(unittest.TestCase):
    def setUp(self):
        self.sub_math = Subject("MTH101", "Mathematics", 95, 100, 40)
        self.sub_phy = Subject("PHY102", "Physics", 85, 100, 40)
        self.sub_chem = Subject("CHM103", "Chemistry", 75, 100, 40)

    def test_pass_and_percentage(self):
        self.assertTrue(self.sub_math.is_pass)
        self.assertEqual(self.sub_math.percentage, 95.0)

        failing = Subject("BIO104", "Biology", 32, 100, 40)
        self.assertFalse(failing.is_pass)

    def test_validation_errors(self):
        with self.assertRaises(ValueError):
            Subject("TST", "Invalid", 105, 100, 40)
        with self.assertRaises(ValueError):
            Subject("TST", "Invalid", -5, 100, 40)

    def test_student_aggregates(self):
        student = Student("101", "Arjun Patel", "Class 10")
        student.add_subject(self.sub_math)
        student.add_subject(self.sub_phy)
        student.add_subject(self.sub_chem)

        self.assertEqual(student.total_obtained, 255.0)
        self.assertEqual(student.total_max, 300.0)
        self.assertEqual(student.percentage, 85.0)
        self.assertTrue(student.has_passed_all)

    def test_distinction_calculation(self):
        student = Student("101", "Arjun Patel", "Class 10")
        student.add_subject(self.sub_math)
        student.add_subject(self.sub_phy)
        student.add_subject(self.sub_chem)

        summary = get_student_summary(student)
        self.assertEqual(summary["status"], "PASS")
        self.assertEqual(summary["division"], "First Class with Distinction")
        self.assertEqual(summary["cgpa"], 9.0)

    def test_failed_subject_result(self):
        student = Student("103", "Rohan Joseph", "Class 10")
        student.add_subject(self.sub_math)
        failing_sub = Subject("PHY102", "Physics", 32, 100, 40)
        student.add_subject(failing_sub)

        self.assertFalse(student.has_passed_all)
        summary = get_student_summary(student)
        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["division"], "Fail")


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(BuiltinMarksTests)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


# ==============================================================================
# 8. MAIN ENTRY POINT
# ==============================================================================

def main():
    # Handle command-line arguments (for quick debugging or testing)
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        if flag == "--demo":
            students = load_all_students()
            if students:
                # Set a breakpoint on the line below in VS Code debugger
                print_marks_card(students[0])
            return
        elif flag == "--roll" and len(sys.argv) > 2:
            student = find_student(sys.argv[2])
            if student:
                print_marks_card(student)
            else:
                print(f"Student with roll number '{sys.argv[2]}' not found.")
            return
        elif flag == "--test":
            run_tests()
            return

    # Interactive menu loop
    while True:
        show_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            students = load_all_students()
            if students:
                print(f"\nShowing report card for: {students[0].name} (Roll No: {students[0].roll_no})\n")
                print_marks_card(students[0])
        elif choice == "2":
            roll = input("\nEnter Roll Number: ").strip()
            student = find_student(roll)
            if student:
                print()
                print_marks_card(student)
            else:
                print(f"{RED}Student with roll number '{roll}' not found.{RESET}")
        elif choice == "3":
            list_all_students()
        elif choice == "4":
            add_student_interactive()
        elif choice == "5":
            print("\nRunning unit tests...")
            run_tests()
        elif choice == "6":
            print("\nExiting program. Goodbye!")
            break
        else:
            print(f"{RED}Invalid option, please choose 1-6.{RESET}")

        input(f"\n{YELLOW}Press Enter to continue...{RESET}")


if __name__ == "__main__":
    main()
