from pydantic import BaseModel, Field


class SkillGapAnalysis(BaseModel):

    target_career: str

    overall_match_score: int = Field(
        ge=0,
        le=100
    )

    strong_skills: list[str]

    missing_skills: list[str]

    partially_known_skills: list[str]

    priority_skills: list[str]

    recommended_learning: list[str]

    project_recommendations: list[str]

    learning_roadmap: list[str]