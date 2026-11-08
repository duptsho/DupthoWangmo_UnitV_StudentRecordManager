import sys
import re

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QComboBox, QSpinBox, QCheckBox, QRadioButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QProgressBar, QScrollArea, QHeaderView
)
from PyQt6.QtCore import Qt

from student_data import StudentManager


class StudentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = StudentManager()

        self.setWindowTitle("Student Record Manager | Duptho Wangmo | Roll No: 7")
        self.resize(1050, 700)

        self.create_menu()
        self.create_interface()
        self.display_students()
        self.statusBar().showMessage("Ready")

    def create_menu(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction("Exit", self.close)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction("About", self.show_about)

    def create_interface(self):
        central = QWidget()
        self.setCentralWidget(central)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setSpacing(15)
        scroll_area.setWidget(content)

        outer_layout = QVBoxLayout(central)
        outer_layout.addWidget(scroll_area)

        heading = QLabel("Student Record Manager")
        heading.setObjectName("heading")
        subtitle = QLabel("Register, manage and keep track of students")
        main_layout.addWidget(heading)
        main_layout.addWidget(subtitle)

        form_title = QLabel("Student Registration")
        form_title.setObjectName("sectionTitle")
        main_layout.addWidget(form_title)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter student ID")

        self.class_input = QComboBox()
        self.class_input.addItems([
            "Class 7", "Class 8", "Class 9",
            "Class 10", "Class 11", "Class 12"
        ])

        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.other_radio = QRadioButton("Other")
        self.male_radio.setChecked(True)

        gender_layout = QHBoxLayout()
        for radio in (self.male_radio, self.female_radio, self.other_radio):
            gender_layout.addWidget(radio)
        gender_widget = QWidget()
        gender_widget.setLayout(gender_layout)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")

        self.marks_input = QSpinBox()
        self.marks_input.setRange(0, 100)
        self.marks_input.setSuffix(" / 100")

        self.active_checkbox = QCheckBox("Active student")
        self.active_checkbox.setChecked(True)

        grid.addWidget(QLabel("Student Name:"), 0, 0)
        grid.addWidget(self.name_input, 0, 1)
        grid.addWidget(QLabel("Student ID:"), 0, 2)
        grid.addWidget(self.id_input, 0, 3)
        grid.addWidget(QLabel("Class:"), 1, 0)
        grid.addWidget(self.class_input, 1, 1)
        grid.addWidget(QLabel("Gender:"), 1, 2)
        grid.addWidget(gender_widget, 1, 3)
        grid.addWidget(QLabel("Email:"), 2, 0)
        grid.addWidget(self.email_input, 2, 1, 1, 3)
        grid.addWidget(QLabel("Marks:"), 3, 0)
        grid.addWidget(self.marks_input, 3, 1)
        grid.addWidget(self.active_checkbox, 3, 2, 1, 2)
        main_layout.addLayout(grid)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Student")
        self.update_button = QPushButton("Update Student")
        self.delete_button = QPushButton("Delete Student")
        self.clear_button = QPushButton("Clear Form")
        for button in (self.add_button, self.update_button,
                       self.delete_button, self.clear_button):
            button_layout.addWidget(button)
        main_layout.addLayout(button_layout)

        search_title = QLabel("Student Records")
        search_title.setObjectName("sectionTitle")
        main_layout.addWidget(search_title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by student name or ID...")
        main_layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Name", "Student ID", "Class", "Gender",
            "Email", "Marks", "Status"
        ])
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setMinimumHeight(300)
        main_layout.addWidget(self.table)

        self.average_label = QLabel("Average Marks: 0%")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        main_layout.addWidget(self.average_label)
        main_layout.addWidget(self.progress)

        self.add_button.clicked.connect(self.add_student)
        self.update_button.clicked.connect(self.update_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.clear_button.clicked.connect(self.clear_form)
        self.search_input.textChanged.connect(self.search_students)
        self.table.itemSelectionChanged.connect(self.select_student)

    def get_gender(self):
        if self.male_radio.isChecked():
            return "Male"
        if self.female_radio.isChecked():
            return "Female"
        return "Other"

    def get_student_data(self):
        name = self.name_input.text().strip()
        student_id = self.id_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not student_id or not email:
            QMessageBox.warning(
                self, "Missing Information",
                "Please fill in the name, student ID and email fields."
            )
            return None

        # Accept letters, spaces, apostrophes, periods and hyphens.
        if len(name) < 2 or not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", name):
            QMessageBox.warning(
                self, "Invalid Name",
                "Enter a valid name using letters and normal name punctuation."
            )
            return None

        if len(student_id) < 2 or any(ch.isspace() for ch in student_id):
            QMessageBox.warning(
                self, "Invalid Student ID",
                "Student ID must contain at least 2 characters and no spaces."
            )
            return None

        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        if not re.fullmatch(email_pattern, email):
            QMessageBox.warning(
                self, "Invalid Email",
                "Please enter a valid email address."
            )
            return None

        return {
            "name": name,
            "student_id": student_id,
            "student_class": self.class_input.currentText(),
            "gender": self.get_gender(),
            "email": email,
            "marks": self.marks_input.value(),
            "active": self.active_checkbox.isChecked()
        }

    def add_student(self):
        student = self.get_student_data()
        if student is None:
            return

        result = self.manager.add_student(student)
        if result == "added":
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.display_students()
            self.clear_form()
        elif result == "duplicate_id":
            QMessageBox.warning(self, "Duplicate ID", "This student ID already exists.")
        else:
            QMessageBox.warning(self, "Duplicate Email", "This email address is already registered.")

    def display_students(self, students=None):
        if students is None:
            students = self.manager.students

        self.table.setRowCount(0)
        for student in students:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [
                student["name"], student["student_id"],
                student["student_class"], student["gender"],
                student["email"], str(student["marks"]),
                "Active" if student["active"] else "Inactive"
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, column, item)
        self.update_average()

    def search_students(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            self.display_students()
        else:
            self.display_students(self.manager.search_student(keyword))

    def select_student(self):
        row = self.table.currentRow()
        if row < 0:
            return

        student_id = self.table.item(row, 1).text()
        for student in self.manager.students:
            if student["student_id"].casefold() == student_id.casefold():
                self.name_input.setText(student["name"])
                self.id_input.setText(student["student_id"])
                self.class_input.setCurrentText(student["student_class"])
                if student["gender"] == "Male":
                    self.male_radio.setChecked(True)
                elif student["gender"] == "Female":
                    self.female_radio.setChecked(True)
                else:
                    self.other_radio.setChecked(True)
                self.email_input.setText(student["email"])
                self.marks_input.setValue(student["marks"])
                self.active_checkbox.setChecked(student["active"])
                break

    def update_student(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(
                self, "Selection Required",
                "Please select a student from the table first."
            )
            return

        student = self.get_student_data()
        if student is None:
            return

        old_id = self.table.item(selected_row, 1).text()
        result = self.manager.update_student(old_id, student)

        if result == "updated":
            QMessageBox.information(
                self, "Updated", "Student record updated successfully!"
            )
            self.display_students()
            self.clear_form()
        elif result == "duplicate_id":
            QMessageBox.warning(
                self, "Duplicate ID", "Another student already has this ID."
            )
        elif result == "duplicate_email":
            QMessageBox.warning(
                self, "Duplicate Email", "Another student already uses this email."
            )
        else:
            QMessageBox.warning(self, "Not Found", "The student record was not found.")

    def delete_student(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(
                self, "Selection Required", "Please select a student to delete."
            )
            return

        student_id = self.table.item(row, 1).text()
        answer = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this student?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            if self.manager.delete_student(student_id):
                QMessageBox.information(
                    self, "Deleted", "Student record deleted successfully!"
                )
            self.display_students()
            self.clear_form()

    def clear_form(self):
        self.name_input.clear()
        self.id_input.clear()
        self.email_input.clear()
        self.class_input.setCurrentIndex(0)
        self.male_radio.setChecked(True)
        self.marks_input.setValue(0)
        self.active_checkbox.setChecked(True)
        self.table.clearSelection()

    def update_average(self):
        students = self.manager.students
        average = round(
            sum(student["marks"] for student in students) / len(students)
        ) if students else 0
        self.average_label.setText(f"Average Marks: {average}%")
        self.progress.setValue(average)

    def show_about(self):
        QMessageBox.about(
            self, "About",
            "Student Record Manager\n"
            "Developed using Python and PyQt6.\n"
            "Name: Duptho Wangmo\n"
            "Roll Number: 7"
        )


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #F7F3EE;
            color: #443B50;
            font-family: 'Segoe UI';
            font-size: 13px;
        }
        QLabel#heading {
            color: #70528E;
            font-size: 28px;
            font-weight: bold;
            padding: 12px;
        }
        QLabel#sectionTitle {
            color: #70528E;
            font-size: 17px;
            font-weight: bold;
            padding-top: 10px;
        }
        QLineEdit, QComboBox, QSpinBox {
            background-color: white;
            border: 1px solid #D8C9E8;
            border-radius: 7px;
            padding: 9px;
        }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border: 2px solid #9B7BBB;
        }
        QPushButton {
            background-color: #8064A2;
            color: white;
            border: none;
            border-radius: 7px;
            padding: 11px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #6D548B; }
        QTableWidget {
            background-color: white;
            alternate-background-color: #F1EAF6;
            border: 1px solid #D8C9E8;
            border-radius: 7px;
            gridline-color: #E7DDED;
        }
        QHeaderView::section {
            background-color: #8064A2;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        QProgressBar {
            background-color: #EDE5F4;
            border: none;
            border-radius: 6px;
            text-align: center;
            height: 18px;
        }
        QProgressBar::chunk {
            background-color: #8064A2;
            border-radius: 6px;
        }
        QCheckBox, QRadioButton { spacing: 8px; }
        QMenuBar { background-color: #EDE5F4; padding: 5px; }
        QMenuBar::item:selected { background-color: #D8C9E8; }
        QScrollArea { border: none; }
    """)
    window = StudentWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
