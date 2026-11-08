# Student Record Manager

**Developer:** Duptho Wangmo  
**Roll Number:** 7  
**Framework:** Python 3.12 and PyQt6

## Overview
A desktop student record manager for adding, viewing, searching, updating and deleting student records. Records are stored locally in `students.json`.

## Features
- Register a student with name, ID, class, gender, email, marks and active status.
- Prevent duplicate student IDs and email addresses.
- Search by student name or student ID.
- Select a table row to load a record into the form.
- Update and delete selected records.
- Validate required fields, name, ID and email.
- Display average marks.
- Save records in a JSON file so they remain after closing the application.

## Requirements
- Python 3.10 or newer (developed with Python 3.12).
- PyQt6 6.10.0.

## Installation (Windows PowerShell)
1. Open PowerShell in the project folder.
2. Create and activate a virtual environment:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Run the application:

   ```powershell
   py main.py
   ```

If PowerShell blocks activation, run `py -m pip install -r requirements.txt` without activating the environment.

## Project structure
```text
StudentRecordManager/
├── main.py
├── student_data.py
├── students.json
├── requirements.txt
├── README.md
├── partA/
│   ├── hello_tkinter.py
│   ├── hello_pyqt.py
│   ├── hello_kivy.py
│   ├── hello_streamlit_optional.py
│   └── requirements-partA.txt
├── tests/
└── screenshots/
```

## Part A demonstrations
- Tkinter: `py partA/hello_tkinter.py`
- PyQt6: `py partA/hello_pyqt.py`
- Kivy: install `partA/requirements-partA.txt`, then run `py partA/hello_kivy.py`.
- Optional Streamlit: `py -m pip install streamlit`, then `py -m streamlit run partA/hello_streamlit_optional.py`.

Take a screenshot of each running demonstration and save it in `screenshots/`. The Kivy demonstration may require platform-specific setup.

## Data file
`students.json` contains sample records. The application updates this file automatically. Back up this file before deleting or replacing records.

## Testing
Run the logic tests with:

```powershell
py -m unittest discover -s tests -v
```

The GUI must also be tested manually because dialog boxes, layout behaviour and screenshots need a running desktop session.

## AI assistance disclosure
AI assistance was used for debugging suggestions, code review, framework research organisation and drafting parts of the documentation. The developer must review, understand, test and be able to explain all submitted code and must disclose the exact assistance used in the final report according to the course instructions.
