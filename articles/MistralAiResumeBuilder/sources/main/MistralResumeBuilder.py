from dataclasses import dataclass
from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

from mistralai.client import MistralClient


@dataclass
class ResumeData:
    summary: str
    history: str
    education: str
    skills: str


class MistralResumeExtractor:
    _client: MistralClient

    def __init__(self):
        self._client = MistralClient()

    def _ask_mistral(
        self, system_role: str, user_role: str, debug: bool = False
    ) -> str:
        response = self._client.chat(
            model="mistral-tiny",
            messages=[
                ChatMessage(role="system", content=system_role),
                ChatMessage(role="user", content=user_role),
            ],
        )
        content = response.choices[0].message.content
        if debug:
            print("############### DEBUG MISTRAL")
            print(response)
            print("#############################")
        return content

    def _extract_work_history(self, data: str) -> str:
        print("... creating section Work History")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        Extract from the given LinkedIn data all that is relevant to the Work History. 

        The output must be formatted in markdown.

        The output must be exclusively written in English.
        It must be complete and should not contain any hallucination.
        """
        return self._ask_mistral(system_role, data)

    def _extract_education(self, data: str) -> str:
        print("... creating section Education")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        Extract from the given LinkedIn data all that is relevant to the Education. 

        The output must be formatted in markdown and detail every school attended, and every diploma received.
        The output must be exclusively written in English.
        """
        return self._ask_mistral(system_role, data)

    def _extract_skills(self, data: str) -> str:
        print("... creating section Skills")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        Extract from the given LinkedIn data all that is relevant to the technical skills. 

        The output must be formatted in markdown and list every skill, with relevant grouping. 
        Each skill must be given a note from 1 to 5.
        The output must be exclusively written in English.
        """
        return self._ask_mistral(system_role, data)

    def _create_summary(self, data: str) -> str:
        print("... creating summary")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        From the given LinkedIn data, create a powerful resume profile in a few sentences and less than 400 characters.
        The summary must contain: the total number of years of experience, the current job title, the 2 or 3 most important achievements, and the 2 or 3 most important skills. 
        The summary should not be a list of bullet points, but must be actual sentences.
        The output must be exclusively written in English.
        """
        return self._ask_mistral(system_role, data)

    def _extract_resume_data(self, source_file_name: str) -> ResumeData:
        with open(source_file_name, "r") as file:
            data = file.read()
            return ResumeData(
                summary=self._create_summary(data),
                history=self._extract_work_history(data),
                education=self._extract_education(data),
                skills=self._extract_skills(data),
            )

    def create_resume(self, source_file_name: str) -> str:
        data = self._extract_resume_data(source_file_name)
        with open("./resume.md", "w") as file:
            lines = []
            lines.append("# Summary\n")
            lines.append(data.summary)
            lines.append("\n# Work History\n")
            lines.append(data.history)
            lines.append("\n# Education\n")
            lines.append(data.education)
            lines.append("\n# Technical Skills\n")
            lines.append(data.skills)
            file.writelines(lines)
            return "./resume.md"


result_file = MistralResumeExtractor().create_resume(
    "./sources/resources/raw_extract.txt"
)
print("Written resume in", result_file)
