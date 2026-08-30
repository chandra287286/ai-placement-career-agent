from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):

    candidate_name: str

    education: list[str]

    technical_skills: list[str]

    soft_skills: list[str]

    experience: list[str]

    projects: list[str]

    certifications: list[str]

    resume_score: int = Field(
        ge=0,
        le=100
    )

    strengths: list[str]

    weaknesses: list[str]

    missing_information: list[str]

    improvement_suggestions: list[str]