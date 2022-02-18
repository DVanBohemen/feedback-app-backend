from typing import List, Optional

from app.interfaces import CourseStore, FeedbackStore
from app.models import Average, Course, Feedback
from app.services import CourseService, FeedbackService


class FakeCourseStore(CourseStore):
    def __init__(self, course: Optional[Course]):
        self._course = course

    def create_course(self, course: Course):
        self._course = course

    def get_course(self):
        return self._course


class FakeFeedbackStore(FeedbackStore):
    def __init__(self, feedback: List[Feedback]):
        self._feedback = feedback

    def list_feedback(self) -> List[Feedback]:
        return self._feedback

    def add_feedback(self, feedback: Feedback):
        self._feedback.append(feedback)


def test_get_course_returns_course():
    # Given
    expected_course = Course(course_name="A")
    course_store = FakeCourseStore(course=expected_course)

    # When
    course = CourseService(course_store).get_course()

    # Then
    assert course == expected_course


def test_create_course_creates_course():
    # Given
    course = Course(course_name="A")
    course_store = FakeCourseStore(course=None)

    # When
    CourseService(course_store).create_course(course)

    # Then
    assert course_store._course == course


def test_submit_feedback_adds_feedback():
    # Given
    feedback_store = FakeFeedbackStore(feedback=[])

    feedback = Feedback(name="A", score=5, comment="T")

    # When
    FeedbackService(feedback_store).submit_feedback(feedback)

    # Then
    assert feedback_store._feedback == [feedback]


def test_get_average_score_returns_average_score_of_feedback():
    # Given
    feedback_store = FakeFeedbackStore(
        feedback=[
            Feedback(name="A", score=6, comment="T"),
            Feedback(name="B", score=8, comment="T"),
        ]
    )

    # When
    average_score = FeedbackService(feedback_store).get_average_feedback_score()

    # Then
    assert average_score == Average(score=7)
