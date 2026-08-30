from agents.llm_client import generate_structured_response
from agents.schemas import CareerRecommendation


class CareerAgent:

    SYSTEM_PROMPT = """
You are an AI Career Planning Agent.

Analyze the student's profile and recommend the most suitable
career path.

You MUST return ONLY valid JSON matching the provided schema.

Do not add:
- Markdown
- ```json
- Explanations outside JSON
- Extra fields

Analyze:

- Education
- Technical skills
- Soft skills
- Interests
- Experience
- Career goal

Give realistic and practical recommendations.

Never guarantee employment.
"""

    def run(self, student):

        user_prompt = f"""
Analyze this student's profile.

Education:
{student["education"]}

Technical Skills:
{", ".join(student["technical_skills"])}

Soft Skills:
{", ".join(student["soft_skills"])}

Interests:
{", ".join(student["interests"])}

Experience:
{student["experience"]}

Career Goal:
{student["career_goal"]}

Generate the personalized career recommendation.
"""

        return generate_structured_response(
            self.SYSTEM_PROMPT,
            user_prompt,
            CareerRecommendation
        )


def main():

    student = {

        "education":
        "B.Tech Computer Science Engineering",

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

        "interests": [
            "Artificial Intelligence",
            "Generative AI",
            "Software Development"
        ],

        "experience":
        "Built academic machine learning projects",

        "career_goal":
        "Become an AI/ML Engineer"
    }

    print("\nStarting Career Agent...\n")

    agent = CareerAgent()

    result = agent.run(student)

    print("=" * 60)
    print("AI CAREER AGENT")
    print("=" * 60)

    print(result.model_dump_json(indent=2))

    print("=" * 60)


if __name__ == "__main__":
    main()