from unittest.mock import mock_open, patch

from app.models import Course, Feedback
from app.stores import CourseStoreImpl, FeedbackStoreImpl


def test_create_course_writes_course_information():
    # Given
    course = Course(course_name="TEST")

    # When
    with patch("builtins.open", new_callable=mock_open) as mocked_open:
        CourseStoreImpl("ANY").create_course(course=course)

    # Then
    mocked_open.return_value.write.assert_called_once_with('{"course_name": "TEST"}')


def test_get_course_returns_correct_json():
    # Given
    expected_course = Course(course_name="TEST")

    # When
    with patch("builtins.open", new=mock_open(read_data='{"course_name": "TEST"}')):
        course = CourseStoreImpl("ANY").get_course()

    # Then
    assert course == expected_course


def test_list_feedback_returns_list_of_feedback():
    # When
    with patch(
        "builtins.open",
        new=mock_open(
            read_data='[{"name": "A", "score": 5, "comment": "T"}, {"name": "B", "score": 7, "comment": "T"}]'
        ),
    ):
        feedback = FeedbackStoreImpl("ANY").list_feedback()

    # Then
    assert Feedback(name="A", score=5, comment="T") in feedback
    assert Feedback(name="B", score=7, comment="T") in feedback


def test_add_feedback_adds_to_existing_feedback():
    # Given
    feedback = Feedback(name="C", score=10, comment="T")

    # When
    with patch(
        "builtins.open",
        new=mock_open(
            read_data='[{"name": "A", "score": 5, "comment": "T"}, {"name": "B", "score": 7, "comment": "T"}]'
        ),
    ) as mocked_open:
        FeedbackStoreImpl("ANY").add_feedback(feedback)

    # Then
    mocked_open.return_value.write.assert_called_once_with(
        '[{"name": "A", "score": 5, "comment": "T"}, {"name": "B", "score": 7, "comment": "T"}, {"name": "C", "score": 10, "comment": "T"}]'
    )
