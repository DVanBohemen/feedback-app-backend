from pydantic import BaseModel, Field


class Feedback(BaseModel):
    name: str = Field(alias="name")
    score: int = Field(alias="score")
    comment: str = Field(alias="comment")

    class Config:
        allow_population_by_field_name = True


class Course(BaseModel):
    course_name: str = Field(alias="courseName")

    class Config:
        allow_population_by_field_name = True


class Average(BaseModel):
    score: float = Field(alias="score")

    class Config:
        allow_population_by_field_name = True
