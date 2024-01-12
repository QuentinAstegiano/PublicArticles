import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatGptEditor:
    _client = OpenAI()

    def ask_gpt(self, system_role: str, query: str) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_role,
                },
                {"role": "user", "content": query},
            ],
        )
        return completion.choices[0].message.content

    def generate_subtitle(self, content: str) -> str:
        print("Generating subtitle...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            Propose a great introduction to the following article, that would grab a reader attention.
            The introduction must be less than 200 characters long.
        """
        return self.ask_gpt(role, content)

    def generate_title(self, content: str) -> str:
        print("Generating title...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            What would be a good title for this article ?
        """
        return self.ask_gpt(role, content)

    def generate_review(self, content: str) -> str:
        print("Generating editor review...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            Review the provided article correct the writing mistakes and reformulate when necessary.
        """
        return self.ask_gpt(role, content)

    def edit_article(self, editor_file: str) -> str:
        print(f"Editing article {editor_file}")
        with open(editor_file, "r") as file:
            content = file.read()
            edited_content = self.generate_review(content)
            title = self.generate_title(edited_content)
            subtitle = self.generate_subtitle(edited_content)

            final_content = f"# {title}\n" + subtitle + "\n\n" + edited_content

            splitted = editor_file.split(os.sep)
            target = os.sep.join(splitted[0:-1]) + os.sep + f"reviews_{splitted[-1]}"
            with open(target, "w") as target_file:
                target_file.write(final_content)
            return target


ChatGptEditor().edit_article(sys.argv[1])
