from agents.llm_client import generate_structured_response
from agents.skill_gap_schema import SkillGapAnalysis


class SkillGapAgent:

    SYSTEM_PROMPT = """
You are the Skill Gap Analysis Agent in an
AI Powered Placement and Career Agent system.

Your job is to compare a student's current skills
with the skills required for their target career.

Analyze:

- Current technical skills
- Current soft skills
- Experience
- Target career
- Required career skills

Identify:

1. Strong skills
2. Missing skills
3. Partially known skills
4. Priority skills
5. Recommended learning
6. Project recommendations
7. Learning roadmap

Calculate an overall match score from 0 to 100.

Be realistic and practical.

Return ONLY valid JSON matching the provided schema.
Do not return Markdown.
Do not use ```json.
Do not add extra fields.
"""

    def analyze(
        self,
        student,
        target_career,
        career_requirements
    ):

        user_prompt = f"""
Analyze this student's skill gap.

STUDENT:

Technical Skills:
{", ".join(student["technical_skills"])}

Soft Skills:
{", ".join(student["soft_skills"])}

Experience:
{student["experience"]}


TARGET CAREER:

{target_career}


REQUIRED SKILLS:

{", ".join(career_requirements)}


Compare the student's current skills with
the target career requirements.

Identify what the student already knows,
what is missing, and what should be learned first.

Create a practical learning roadmap.
"""

        return generate_structured_response(
            self.SYSTEM_PROMPT,
            user_prompt,
            SkillGapAnalysis
        )


def main():

    student = {

        "technical_skills": [
            "Python",
            "Java",
            "Machine Learning",
            "SQL"
        ],

        "soft_skills": [
            "Communication",
            "Problem Solving",
            "Teamwork"
        ],

        "experience":
        "Built academic machine learning projects"
    }

    target_career = "AI/ML Engineer"

    career_requirements = [

        "Python",
        "Machine Learning",
        "Deep Learning",
        "PyTorch",
        "TensorFlow",
        "SQL",
        "Generative AI",
        "LLMs",
        "MLOps",
        "Docker",
        "Cloud Computing"

    ]

    print("\nStarting Skill Gap Agent...\n")

    agent = SkillGapAgent()

    result = agent.analyze(
        student,
        target_career,
        career_requirements
    )

    print("=" * 60)
    print("SKILL GAP ANALYSIS")
    print("=" * 60)

    print(result.model_dump_json(indent=2))

    print("=" * 60)


if __name__ == "__main__":
    main()