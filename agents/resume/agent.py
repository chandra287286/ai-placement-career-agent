from pypdf import PdfReader

from agents.llm_client import generate_structured_response
from agents.resume_schema import ResumeAnalysis


class ResumeAgent:

    SYSTEM_PROMPT = """
You are an AI Resume Analysis Agent in an
AI Powered Placement and Career Agent system.

Your job is to analyze a student's resume.

Extract and analyze:

- Candidate name
- Education
- Technical skills
- Soft skills
- Experience
- Projects
- Certifications

Then evaluate:

- Resume score from 0 to 100
- Strengths
- Weaknesses
- Missing information
- Improvement suggestions

Focus on information actually present in the resume.

Do not invent candidate information.

Return ONLY valid JSON matching the provided schema.
Do not return Markdown.
Do not use ```json.
Do not add extra fields.
"""

    def extract_text(self, pdf_path):

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text


    def analyze(self, pdf_path):

        resume_text = self.extract_text(pdf_path)

        if not resume_text.strip():
            raise ValueError(
                "Could not extract text from the resume."
            )

        user_prompt = f"""
Analyze the following resume.

---------------- RESUME ----------------

{resume_text}

-------------- END RESUME --------------

Extract the candidate information and provide
a detailed resume analysis.
"""

        return generate_structured_response(
            self.SYSTEM_PROMPT,
            user_prompt,
            ResumeAnalysis
        )


def main():

    # Change this to your actual resume file
    resume_path = "data/resume.pdf"

    print("\nStarting Resume Agent...\n")

    agent = ResumeAgent()

    result = agent.analyze(resume_path)

    print("=" * 60)
    print("RESUME ANALYSIS")
    print("=" * 60)

    print(result.model_dump_json(indent=2))

    print("=" * 60)


if __name__ == "__main__":
    main()