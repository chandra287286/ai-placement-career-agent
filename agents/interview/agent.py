from agents.llm_client import generate_structured_response
from agents.interview_schema import InterviewPlan


class InterviewAgent:

    SYSTEM_PROMPT = """
You are an AI Interview Preparation Agent in an
AI Powered Placement and Career Agent system.

Your job is to create a personalized interview
preparation plan for a student.

Analyze:

- Target career
- Student technical skills
- Student projects
- Student experience
- Skill gaps
- Target job requirements

Generate:

1. Technical topics
2. Coding topics
3. Project discussion topics
4. HR topics
5. Technical interview questions
6. Coding interview questions
7. Project-based questions
8. HR questions
9. Preparation roadmap

For every question provide:

- Question
- Category
- Difficulty
- Expected topics

Give a preparation score from 0 to 100.

Questions should be realistic for entry-level
placement interviews.

Do not invent experience that the student does not have.

Return ONLY valid JSON matching the provided schema.
Do not return Markdown.
Do not use ```json.
Do not add extra fields.
"""


    def prepare(
        self,
        student,
        target_role,
        skill_gaps,
        job_requirements
    ):

        user_prompt = f"""
Create an interview preparation plan.

TARGET ROLE:
{target_role}


STUDENT TECHNICAL SKILLS:

{", ".join(student["technical_skills"])}


STUDENT SOFT SKILLS:

{", ".join(student["soft_skills"])}


STUDENT EXPERIENCE:

{student["experience"]}


SKILL GAPS:

{", ".join(skill_gaps)}


TARGET JOB REQUIREMENTS:

{", ".join(job_requirements)}


Create a personalized interview preparation
plan based on this information.

Focus especially on topics that are likely
to be asked for an entry-level AI/ML Engineer.
"""

        return generate_structured_response(
            self.SYSTEM_PROMPT,
            user_prompt,
            InterviewPlan
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


    target_role = "AI/ML Engineer"


    skill_gaps = [

        "Deep Learning",
        "PyTorch",
        "Generative AI",
        "LLMs",
        "MLOps",
        "Docker"

    ]


    job_requirements = [

        "Python",
        "Machine Learning",
        "Deep Learning",
        "PyTorch",
        "SQL",
        "Generative AI",
        "LLMs",
        "Docker"

    ]


    print("\nStarting Interview Agent...\n")


    agent = InterviewAgent()


    result = agent.prepare(
        student,
        target_role,
        skill_gaps,
        job_requirements
    )


    print("=" * 60)
    print("INTERVIEW PREPARATION PLAN")
    print("=" * 60)


    print(
        result.model_dump_json(indent=2)
    )


    print("=" * 60)


if __name__ == "__main__":
    main()