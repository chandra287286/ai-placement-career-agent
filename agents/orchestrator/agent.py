import json

from agents.resume.agent import ResumeAgent
from agents.career_agent import CareerAgent
from agents.skill_gap.agent import SkillGapAgent
from agents.job.agent import JobMatchingAgent
from agents.interview.agent import InterviewAgent


class CareerOrchestrator:

    def __init__(self):

        self.resume_agent = ResumeAgent()
        self.career_agent = CareerAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.job_agent = JobMatchingAgent()
        self.interview_agent = InterviewAgent()


    def run(self, resume_path):

        print("\n" + "=" * 70)
        print("AI PLACEMENT & CAREER AGENT")
        print("=" * 70)


        # ============================================================
        # STEP 1 — RESUME AGENT
        # ============================================================

        print("\n[1/5] Running Resume Agent...")

        resume_result = self.resume_agent.analyze(
            resume_path
        )

        print("✓ Resume analysis completed")


        # ============================================================
        # CREATE STUDENT PROFILE
        # ============================================================

        student = {

            "education":
                ", ".join(resume_result.education)
                if resume_result.education
                else "Not specified",

            "technical_skills":
                resume_result.technical_skills,

            "soft_skills":
                resume_result.soft_skills,

            "interests": [
                "Artificial Intelligence",
                "Machine Learning",
                "Generative AI"
            ],

            "experience":
                " ".join(resume_result.experience)
                if resume_result.experience
                else "No professional experience",

            "career_goal":
                "Find the most suitable career based on my resume"
        }


        # ============================================================
        # STEP 2 — CAREER AGENT
        # ============================================================

        print("\n[2/5] Running Career Agent...")

        career_result = self.career_agent.run(
            student
        )

        target_career = career_result.recommended_career

        print(
            f"✓ Recommended Career: {target_career}"
        )


        # ============================================================
        # STEP 3 — SKILL GAP AGENT
        # ============================================================

        print("\n[3/5] Running Skill Gap Agent...")

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


        skill_gap_result = self.skill_gap_agent.analyze(

            student,

            target_career,

            career_requirements

        )

        print("✓ Skill gap analysis completed")


        # ============================================================
        # STEP 4 — JOB MATCHING AGENT
        # ============================================================

        print("\n[4/5] Running Job Matching Agent...")

        jobs = self.job_agent.load_jobs(
            "data/jobs.json"
        )


        job_result = self.job_agent.match_jobs(

            student,

            target_career,

            jobs

        )

        print("✓ Job matching completed")


        # ============================================================
        # STEP 5 — INTERVIEW AGENT
        # ============================================================

        print("\n[5/5] Running Interview Agent...")

        interview_result = self.interview_agent.prepare(

            student,

            target_career,

            skill_gap_result.missing_skills,

            career_requirements

        )

        print("✓ Interview preparation completed")


        # ============================================================
        # FINAL CAREER PLAN
        # ============================================================

        final_result = {

            "candidate":
                resume_result.candidate_name,

            "target_career":
                target_career,

            "career_fit_score":
                career_result.career_fit_score,

            "resume_score":
                resume_result.resume_score,

            "skill_match_score":
                skill_gap_result.overall_match_score,

            "strong_skills":
                skill_gap_result.strong_skills,

            "skill_gaps":
                skill_gap_result.missing_skills,

            "priority_skills":
                skill_gap_result.priority_skills,

            "recommended_jobs":
                [
                    job.model_dump()
                    for job in job_result.recommended_jobs
                ],

            "interview_preparation":
                interview_result.model_dump(),

            "career_action_plan":
                career_result.action_plan

        }


        return final_result


def main():

    resume_path = "data/resume.pdf"

    orchestrator = CareerOrchestrator()

    result = orchestrator.run(
        resume_path
    )

    print("\n")
    print("=" * 70)
    print("FINAL AI CAREER PLAN")
    print("=" * 70)

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    print("=" * 70)


if __name__ == "__main__":
    main()