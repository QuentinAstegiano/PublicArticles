from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


class TestGenerator:
    _client = OpenAI()

    def call_gpt(self, content: str) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You're an expert Python developper, who can use the pytest library to write useful and meaningful tests in python.
                        Write the tests for this file. Output only the tests, and no textual explanations. Comments are allowed, if necessary.""",
                },
                {"role": "user", "content": content},
            ],
        )
        return completion.choices[0].message.content

    def get_file_content(self, source: str) -> str:
        with open(source, "r") as file:
            content = file.read()
            return content

    def generate(self, source: str) -> str:
        content = self.get_file_content(source)
        return self.call_gpt(content)

    def create_test_file(self, source: str) -> str:
        content = self.generate(source)
        splitted = source.split(os.sep)
        target = os.sep.join(splitted[0:-1]) + os.sep + f"test_{splitted[-1]}"
        with open(target, "w") as file:
            file.write(content)
        return target
