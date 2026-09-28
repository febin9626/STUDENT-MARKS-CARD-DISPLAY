# Student Marks Card System (Python)

This is a simple Python project I made to calculate and display student marks cards in the terminal.

It takes student details and subject marks, then automatically calculates the total marks, percentage, CGPA (on a 10-point scale), grades, and pass/fail division. It prints everything in a neat, aligned marks card format.

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
- **Interactive Menu**:
  1. Quick Demo to see a sample student marks card directly.
  2. Search student by roll number.
  3. View all students list with total marks, percentage, and status.
  4. Add new student details and enter marks.
  5. Run the built-in unit tests.
- **Pure Python Storage**: All student records are stored directly inside `students_data.py` (no JSON or external database needed).

---

## How to Run & Debug in VS Code

You can run and debug this directly in VS Code without any extra setup:

1. Open this project folder in VS Code.
2. Open `student_marks_card.py`.
3. Click to the left of any line number to put a red breakpoint dot.
4. Press **F5** (or click **Run > Start Debugging**).
5. The terminal will open at the bottom where you can type your choices (1 to 6) and test everything step by step!

---

## Running from Terminal

If you want to run it from command prompt or terminal directly:

```bash
# Run the main interactive menu
python3 student_marks_card.py

# Quick demo (shows sample marks card for Roll 101)
python3 student_marks_card.py --demo

# Search a student directly by roll number
python3 student_marks_card.py --roll 101

# Run unit tests to verify everything is working fine
python3 student_marks_card.py --test
# or
python3 test_marks.py -v
```

---

## Grading Table

| Marks Range (%) | Grade | Grade Point |   Remarks    |
________________________________________________________
| 90% and above   | A+    | 10.0        | Outstanding  |
| 80% to 89%      | A     | 9.0         | Excellent    |
| 70% to 79%      | B+    | 8.0         | Very Good    |
| 60% to 69%      | B     | 7.0         | Good         |
| 50% to 59%      | C     | 6.0         | Average      |
| 40% to 49%      | D     | 5.0         | Satisfactory |
| Below 40%       | F     | 0.0         | Fail         |

---

## Project Files

- `student_marks_card.py` - Main code containing all classes, grading logic, and terminal menu.
- `students_data.py` - Contains the saved student data in simple Python format.
- `main.py` - Simple launcher file.
- `test_marks.py` - Unit test cases to test the grading calculations.
