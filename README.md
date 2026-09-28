# Student Marks Card System (Python)

This is a simple Python project I made to calculate and display student marks cards in the terminal for the Python Essentials course project.

It takes student details and subject marks, then automatically calculates the total marks, percentage, CGPA (on a 10-point scale), grades, and pass/fail division. It prints everything in a neat, aligned marks card format.

---

## 1. Environment Setup

To run this project, you just need Python 3 installed on your system:

- **Python Version**: Python 3.8 or higher (Python 3.10 / 3.11 / 3.12 works great).
- **Supported Operating Systems**: Windows, macOS, or Linux (Ubuntu, Debian, Fedora, etc.).
- **Verify Python Installation**:
  Open your command prompt or terminal and check if Python is installed:
  ```bash
  python3 --version
  # or on Windows:
  python --version
  ```

---

## 2. Dependency Installation

- **No external dependencies or third-party libraries needed!**
- This project is developed completely using Python's standard built-in libraries (`sys`, `unittest`, `dataclasses`, `typing`).
- You **do not** need to run `pip install` or download any extra packages. Everything runs out of the box with standard Python.

---

## 3. Configuration

The project comes pre-configured and ready to run:

- **Student Data File (`students_data.py`)**: Contains default sample student records (Roll 101, 102, 103, 104). You can add new students using Option 4 in the interactive terminal menu or by directly editing `students_data.py`.
- **Passing Threshold**: Minimum passing mark is configured as 40 out of 100 for each subject. If a student scores below 40 in any subject, their overall result is marked as FAIL.
- **Grading Scale**: Standard 10-point CGPA system (A+ = 10.0, A = 9.0, B+ = 8.0, B = 7.0, C = 6.0, D = 5.0, F = 0.0).

---

## 4. Execution (How to Run)

The project is fully executable via the command line without requiring any GUI setup.

### Option A: Run Interactive Terminal Menu
Open your terminal inside the project folder and run:
```bash
python3 student_marks_card.py
# or
python3 main.py
```
This starts the interactive menu where you can:
1. View a Quick Demo marks card
2. Search a student by Roll Number
3. View all students in the database
4. Add new student details and enter marks
5. Run unit tests
6. Exit

### Option B: Run with Direct Command Line Flags
You can also run specific tasks directly without navigating the interactive menu:
```bash
# 1. Quick demo (shows sample marks card for Roll 101)
python3 student_marks_card.py --demo

# 2. Search a student directly by roll number
python3 student_marks_card.py --roll 101

# 3. Run built-in unit tests
python3 student_marks_card.py --test
# or directly with python's test runner
python3 test_marks.py -v
```

### Option C: Run & Debug in VS Code
1. Open this project folder in VS Code.
2. Open `student_marks_card.py`.
3. Click to the left of any line number to place a breakpoint if you want to inspect variables.
4. Press **F5** (or click **Run > Start Debugging**).
5. The terminal opens at the bottom where you can type your choices and test the application step by step.

---

## What This Project Does

- **Neat Marks Card Table**: Prints student details, individual marks, pass/fail status, total marks, percentage, and 10-point CGPA in an aligned box table.
- **Passing & Grading Rules**:
  - Pass mark is kept as 40 out of 100 for each subject.
  - If a student gets less than 40 in even one subject, their overall result will be shown as **FAIL** with a note for supplementary / re-exam.
  - Divisions are given based on standard Indian college/board rules:
    - **First Class with Distinction**: 75% and above
    - **First Class**: 60% to 74%
    - **Second Class**: 50% to 59%
    - **Pass Class**: 40% to 49%
    - **Fail**: Below 40% or failed in any subject
- **Pure Python Storage**: All student records are stored directly inside `students_data.py` (no JSON or external database needed).

---

## Grading Table

| Marks Range (%) | Grade | Grade Point | Remarks |
|:---:|:---:|:---:|---|
| 90% and above | A+ | 10.0 | Outstanding |
| 80% to 89% | A | 9.0 | Excellent |
| 70% to 79% | B+ | 8.0 | Very Good |
| 60% to 69% | B | 7.0 | Good |
| 50% to 59% | C | 6.0 | Average |
| 40% to 49% | D | 5.0 | Satisfactory |
| Below 40% | F | 0.0 | Fail |

---

## Project Files

- `student_marks_card.py` - Main code containing all classes, grading logic, and terminal menu.
- `students_data.py` - Contains the saved student data in simple Python format.
- `main.py` - Simple launcher file.
- `test_marks.py` - Unit test cases to test the grading calculations.
