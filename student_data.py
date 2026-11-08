import json
from pathlib import Path


class StudentManager:
    """Handles student records and JSON file storage."""

    def __init__(self):
        self.file_path = Path(__file__).with_name("students.json")
        self.students = self.load_students()

    def load_students(self):
        if self.file_path.exists():
            try:
                with self.file_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                return data if isinstance(data, list) else []
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def save_students(self):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=4, ensure_ascii=False)

    def add_student(self, student):
        new_id = student["student_id"].casefold()
        new_email = student["email"].casefold()

        for existing in self.students:
            if existing["student_id"].casefold() == new_id:
                return "duplicate_id"
            if existing["email"].casefold() == new_email:
                return "duplicate_email"

        self.students.append(student)
        self.save_students()
        return "added"

    def update_student(self, student_id, updated_data):
        target = None
        for student in self.students:
            if student["student_id"].casefold() == student_id.casefold():
                target = student
                break

        if target is None:
            return "not_found"

        new_id = updated_data["student_id"].casefold()
        new_email = updated_data["email"].casefold()

        for existing in self.students:
            if existing is target:
                continue
            if existing["student_id"].casefold() == new_id:
                return "duplicate_id"
            if existing["email"].casefold() == new_email:
                return "duplicate_email"

        target.update(updated_data)
        self.save_students()
        return "updated"

    def delete_student(self, student_id):
        for student in self.students:
            if student["student_id"].casefold() == student_id.casefold():
                self.students.remove(student)
                self.save_students()
                return True
        return False

    def search_student(self, keyword):
        keyword = keyword.casefold().strip()
        if not keyword:
            return list(self.students)

        return [
            student for student in self.students
            if keyword in student["name"].casefold()
            or keyword in student["student_id"].casefold()
        ]
