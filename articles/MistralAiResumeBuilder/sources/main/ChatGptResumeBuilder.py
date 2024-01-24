from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatGPTResumeExtractor:
    _client = OpenAI()

    def _ask_chatgpt(self, system_role: str, user_role: str) -> str:
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_role},
            ],
        )
        content = response.choices[0].message.content
        return content

    def _extract_profesionnal_history(self, data: str) -> str:
        print("... creating section professional history")
        system_role = """
        You're an helpful assistant specialized in writing comprehensive resume.
        Extract from the given LinkedIn data all that is relevant to the Professionnal History. 
        It should be grouped by company ; and for each company, every role held in that company should be listed.
        For each role, detail what was done and the associated skills.

        The output must be formatted in markdown.

        The output must be exclusively written in English. Words not in english should be translated.
        """
        return self._ask_chatgpt(system_role, data)

    def _extract_educational_history(self, data: str) -> str:
        print("... creating section educational history")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        Extract from the given LinkedIn data all that is relevant to the educational history. 
        The output must be formatted in markdown and detail every school attended, and every diploma received.
        It should not contain anything not related to the educational history.

        The output must be exclusively written in English. Words not in english should be translated.
        """
        return self._ask_chatgpt(system_role, data)

    def _extract_skills(self, data: str) -> str:
        print("... creating section Skills")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        Extract from the given LinkedIn data all that is relevant to the technical skills. 

        The output must be formatted in markdown and list every skill, with relevant grouping. 
        Each skill must be given a note from 1 to 5.

        The output must be exclusively written in English. Words not in english should be translated.
        """
        return self._ask_chatgpt(system_role, data)

    def _create_summary(self, data: str) -> str:
        print("... creating summary")
        system_role = """
        You're an helpful assistant specialized in writing resume.
        From the given LinkedIn data, create a powerful resume profile in a few sentences and less than 400 characters.
        The summary must contain: the total number of years of experience, the current job title, the 2 or 3 most important achievements, and the 2 or 3 most important skills. 
        The summary should not be a list of bullet points, but must be actual sentences.
        The output must be exclusively written in English.
        """
        return self._ask_chatgpt(system_role, data)

    def create_resume(self, source_file_name: str) -> str:
        with open(source_file_name, "r") as source_file:
            with open("./resume_chatgpt.md", "w") as target_file:
                data = source_file.read()
                target_file.write("# Summary\n")
                target_file.write(self._create_summary(data))
                target_file.write("\n# Professional History\n")
                target_file.write(self._extract_profesionnal_history(data))
                target_file.write("\n# Educational History\n")
                target_file.write(self._extract_educational_history(data))
                target_file.write("\n# Technical Skills\n")
                target_file.write(self._extract_skills(data))
                return target_file.name


result_file = ChatGPTResumeExtractor().create_resume(
    "./sources/resources/raw_extract.txt"
)
print("Written resume in", result_file)
