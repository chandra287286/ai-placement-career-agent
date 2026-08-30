from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):

    question: str

    category: str

    difficulty: str

    expected_topics: list[str]


class InterviewPlan(BaseModel):

    target_role: str

    preparation_score: int = Field(
        ge=0,
        le=100
    )

    technical_topics: list[str]

    coding_topics: list[str]

    project_topics: list[str]

    hr_topics: list[str]

    technical_questions: list[InterviewQuestion]

    coding_questions: list[InterviewQuestion]

    project_questions: list[InterviewQuestion]

    hr_questions: list[InterviewQuestion]

    preparation_roadmap: list[str]