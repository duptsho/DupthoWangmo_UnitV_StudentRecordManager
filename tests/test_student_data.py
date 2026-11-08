import json
import tempfile
import unittest
from pathlib import Path

from student_data import StudentManager


def sample(student_id="S001", email="one@example.com", name="Karma Dorji"):
    return {
        "name": name,
        "student_id": student_id,
        "student_class": "Class 9",
        "gender": "Male",
        "email": email,
        "marks": 80,
        "active": True,
    }


class StudentManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manager = StudentManager()
        self.manager.file_path = Path(self.temp_dir.name) / "students.json"
        self.manager.students = []

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_student(self):
        self.assertEqual(self.manager.add_student(sample()), "added")
        self.assertEqual(len(self.manager.students), 1)

    def test_reject_duplicate_id_case_insensitive(self):
        self.manager.add_student(sample())
        self.assertEqual(
            self.manager.add_student(sample(student_id="s001", email="two@example.com")),
            "duplicate_id"
        )

    def test_reject_duplicate_email_case_insensitive(self):
        self.manager.add_student(sample())
        self.assertEqual(
            self.manager.add_student(sample(student_id="S002", email="ONE@example.com")),
            "duplicate_email"
        )

    def test_search_by_name(self):
        self.manager.add_student(sample())
        self.assertEqual(len(self.manager.search_student("karma")), 1)

    def test_search_by_id(self):
        self.manager.add_student(sample())
        self.assertEqual(len(self.manager.search_student("s001")), 1)

    def test_search_no_match(self):
        self.manager.add_student(sample())
        self.assertEqual(self.manager.search_student("missing"), [])

    def test_update_student(self):
        self.manager.add_student(sample())
        changed = sample(name="Karma Updated")
        self.assertEqual(self.manager.update_student("S001", changed), "updated")
        self.assertEqual(self.manager.students[0]["name"], "Karma Updated")

    def test_update_rejects_duplicate_email(self):
        self.manager.add_student(sample())
        self.manager.add_student(sample(student_id="S002", email="two@example.com"))
        self.assertEqual(
            self.manager.update_student("S001", sample(email="two@example.com")),
            "duplicate_email"
        )

    def test_delete_student(self):
        self.manager.add_student(sample())
        self.assertTrue(self.manager.delete_student("S001"))
        self.assertEqual(self.manager.students, [])

    def test_persistence(self):
        self.manager.add_student(sample())
        loaded = self.manager.load_students()
        self.assertEqual(loaded[0]["student_id"], "S001")


if __name__ == "__main__":
    unittest.main()
