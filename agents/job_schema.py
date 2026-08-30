from pydantic import BaseModel, Field


class JobMatch(BaseModel):

    job_title: str

    company: str

    match_score: int = Field(
        ge=0,
        le=100
    )

    matching_skills: list[str]

    missing_skills: list[str]

    match_explanation: str

    recommendation: str


class JobMatchingResult(BaseModel):

    target_career: str

    jobs_analyzed: int

    recommended_jobs: list[JobMatch]