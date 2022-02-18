from unittest.mock import Mock

from fastapi.testclient import TestClient

from app import main
from app.main import app
from app.models import Average, Course, Feedback
from app.services import CourseService, FeedbackService

client = TestClient(app)


def test_get_health():
    # When
    response = client.get("/health")

    # Then
    assert response.status_code == 200
    assert response.json() == {"status": "up"}


def test_get_course():
    # Given
    mocked_course_service = Mock(spec=CourseService)
    mocked_course_service.get_course.return_value = Course(course_name="TEST")
    main.get_course_service = lambda: mocked_course_service

    # When
    response = client.get("/course")

    # Then
    assert response.status_code == 200
    assert response.json() == {"courseName": "TEST"}


def test_post_course():
    # Given
    mocked_course_service = Mock(spec=CourseService)
    main.get_course_service = lambda: mocked_course_service

    expected_course = Course(course_name="TEST")
    post_json = {"courseName": "TEST"}

    # When
    response = client.post("/course", json=post_json)

    # Then
    assert response.status_code == 200
    mocked_course_service.create_course.assert_called_once_with(expected_course)


def test_post_course_feedback():
    # Given
    mocked_feedback_service = Mock(spec=FeedbackService)
    main.get_feedback_service = lambda: mocked_feedback_service

    expected_feedback = Feedback(name="TEST", score=7, comment="T")
    post_json = {"name": "TEST", "score": 7, "comment": "T"}

    # When
    client.post("/course/feedback", json=post_json)

    # Then
    mocked_feedback_service.submit_feedback.assert_called_once_with(expected_feedback)


def test_get_course_score():
    # Given
    mocked_feedback_service = Mock(spec=FeedbackService)
    mocked_feedback_service.get_average_feedback_score = lambda: Average(score=7)

    main.get_feedback_service = lambda: mocked_feedback_service

    # When
    response = client.get("/course/average")

    # Then
    assert response.status_code == 200
    assert response.json() == {"score": 7}
