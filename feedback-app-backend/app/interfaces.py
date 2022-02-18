from abc import ABC
from typing import List, Optional

from app.models import Course, Feedback


class CourseStore(ABC):
    def create_course(self, course: Course):
        ...

    def get_course(self) -> Optional[Course]:
        ...


class FeedbackStore(ABC):
    def add_feedback(self, feedback: Feedback):
        ...

    def list_feedback(self) -> List[Feedback]:
        ...
