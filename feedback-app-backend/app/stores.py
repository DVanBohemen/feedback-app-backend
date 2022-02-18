from typing import List, Optional

from pydantic import parse_raw_as

from app.interfaces import CourseStore, FeedbackStore
from app.models import Course, Feedback


class CourseStoreImpl(CourseStore):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def create_course(self, course: Course):
        with open(self._file_path, "w") as file:
            file.write(course.json())

    def get_course(self) -> Optional[Course]:
        try:
            with open(self._file_path, "r") as file:
                course = file.read()
                return parse_raw_as(Course, course)
        except FileNotFoundError:
            return None


class FeedbackStoreImpl(FeedbackStore):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def list_feedback(self) -> List[Feedback]:
        try:
            with open(self._file_path, "r") as file:
                feedback = file.read()
                return parse_raw_as(List[Feedback], feedback)
        except FileNotFoundError:
            return []

    def add_feedback(self, feedback: Feedback):
        existing_feedback_list = self.list_feedback()
        new_feedback_list = existing_feedback_list + [feedback]

        self._write_feedback(new_feedback_list)

    def _write_feedback(self, feedback: List[Feedback]):
        try:
            s = "[" + ", ".join([f.json() for f in feedback]) + "]"

            with open(self._file_path, "w") as file:
                file.write(s)
        except FileNotFoundError as e:
            print(f"Failed to write file with error: {e}")
