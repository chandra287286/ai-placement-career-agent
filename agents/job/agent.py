import json

from agents.llm_client import generate_structured_response
from agents.job_schema import JobMatchingResult


class JobMatchingAgent:

    SYSTEM_PROMPT = """
You are an AI Job Matching Agent in an
AI Powered Placement and Career Agent system.

Your job is to compare a student's skills with
available job opportunities.

For every job:

1. Calculate a match score from 0 to 100.
2. Identify matching skills.
3. Identify missing skills.
4. Explain why the student matches the job.
5. Give a recommendation.

Recommendations should be one of:

- Strong Match
- Good Match
- Partial Match
- Low Match

Rank the jobs from best match to lowest match.

Be realistic.

Do not guarantee employment.

Return ONLY valid JSON matching the provided schema.
Do not return Markdown.
Do not use ```json.
Do not add extra fields.
"""

    def load_jobs(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def match_jobs(
        self,
        student,
        target_career,
        jobs
    ):

        job_information = ""

        for index, job in enumerate(jobs, start=1):

            job_information += f"""
JOB {index}

Title:
{job["job_title"]}

Company:
{job["company"]}

Required Skills:
{", ".join(job["required_skills"])}

Description:
{job["description"]}

--------------------------
"""


        user_prompt = f"""
Analyze the following student's profile.

TARGET CAREER:
{target_career}

STUDENT TECHNICAL SKILLS:
{", ".join(student["technical_skills"])}

STUDENT SOFT SKILLS:
{", ".join(student["soft_skills"])}

EXPERIENCE:
{student["experience"]}


AVAILABLE JOBS:

{job_information}


Compare the student with every available job.

Rank the jobs according to suitability.

Return the complete job matching analysis.
"""

        return generate_structured_response(
            self.SYSTEM_PROMPT,
            user_prompt,
            JobMatchingResult
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


    jobs_file = "data/jobs.json"


    print("\nStarting Job Matching Agent...\n")


    agent = JobMatchingAgent()


    jobs = agent.load_jobs(jobs_file)


    result = agent.match_jobs(
        student,
        target_career,
        jobs
    )


    print("=" * 60)
    print("JOB MATCHING RESULTS")
    print("=" * 60)


    print(
        result.model_dump_json(indent=2)
    )


    print("=" * 60)


if __name__ == "__main__":
    main()