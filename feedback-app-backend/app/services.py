from app.models import Average, Course, Feedback
from app.stores import CourseStore, FeedbackStore


class CourseService:
    def __init__(self, course_store: CourseStore):
        self._course_store = course_store

    def get_course(self) -> Course:
        return self._course_store.get_course()

    def create_course(self, course: Course):
        self._course_store.create_course(course)


class FeedbackService:
    def __init__(self, feedback_store: FeedbackStore):
        self._feedback_store = feedback_store

    def submit_feedback(self, feedback: Feedback):
        existing_feedback = self._feedback_store.list_feedback()

        if feedback.name not in [f.name for f in existing_feedback]:
            self._feedback_store.add_feedback(feedback)

    def get_average_feedback_score(self) -> Average:

        try:
            feedback = self._feedback_store.list_feedback()
            score = sum([f.score for f in feedback]) / len(feedback)
        except ZeroDivisionError:
            return Average(score=0)
        return Average(score=score)
