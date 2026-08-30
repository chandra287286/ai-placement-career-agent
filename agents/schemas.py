from pydantic import BaseModel, Field


class CareerRecommendation(BaseModel):
    recommended_career: str = Field(
        description="The most suitable career for the student"
    )

    career_fit_score: int = Field(
        description="Career suitability score from 0 to 100",
        ge=0,
        le=100
    )

    career_fit_explanation: str = Field(
        description="Why the career is suitable"
    )

    strengths: list[str] = Field(
        description="Student's existing strengths"
    )

    skill_gaps: list[str] = Field(
        description="Skills the student is currently missing"
    )

    skills_to_learn: list[str] = Field(
        description="Skills the student should learn"
    )

    recommended_projects: list[str] = Field(
        description="Projects recommended for the student's career"
    )

    action_plan: list[str] = Field(
        description="Step-by-step career action plan"
    )

    placement_tips: list[str] = Field(
        description="Placement preparation tips"
    )