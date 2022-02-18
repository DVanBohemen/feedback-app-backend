from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.models import Average, Course, Feedback
from app.services import CourseService, FeedbackService
from app.stores import CourseStoreImpl, FeedbackStoreImpl

COURSE_FILE_PATH = "course.json"
FEEDBACK_FILE_PATH = "feedback.json"

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:7000",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_feedback_service() -> FeedbackService:
    feedback_store = FeedbackStoreImpl(FEEDBACK_FILE_PATH)
    return FeedbackService(feedback_store=feedback_store)


def get_course_service() -> CourseService:
    course_store = CourseStoreImpl(COURSE_FILE_PATH)
    return CourseService(course_store=course_store)


@app.get("/health")
def root():
    return {"status": "up"}


@app.get("/course", response_model=Course)
async def get_course() -> Course:
    course_service = get_course_service()

    return course_service.get_course()


@app.post("/course", response_model=Course)
async def post_course(course: Course) -> Course:
    course_service = get_course_service()

    course_service.create_course(course)

    return course


@app.post("/course/feedback")
async def post_course_feedback(feedback: Feedback) -> Feedback:
    feedback_service = get_feedback_service()

    feedback_service.submit_feedback(feedback)

    return feedback


@app.get("/course/average", response_model=Average)
async def get_course_score():
    feedback_service = get_feedback_service()

    score = feedback_service.get_average_feedback_score()

    return score
