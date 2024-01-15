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
            Write the best possible title for that article, to grab a reader attention and to maximize engagement.
        """
        title = self.ask_gpt(role, content)
        if title.startswith("#"):
            title = title.replace("#", "")
        return title

    def generate_closing_statement(self, content: str) -> str:
        print("Generating closing statement...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            Write a suitable conclusion for the given article, sumarizing what was written and offering perspective on some next steps.
        """
        return self.ask_gpt(role, content)

    def generate_review(self, content: str) -> str:
        print("Generating editor review...")
        role = """
            You are a skilled editor specialized in technical articles published on the internet.
            Review the provided article, correct any writing mistakes, and reformulate when necessary— even if it involves rewriting entire sentences. Create actual sentences when they are missing.
            Aim to enhance clarity, improve grammar, and refine the overall writing quality.
            Also aim to maximize reader engagement throughout the article. The sections titles can also be rewritten when appropriate.
            When possible, generate additional content to expand on what is written in the article, without changing the original meaning.
            Try not to remove content from the original article ; reformulate when necessary, but keep at least the meaning of what was written.

            Ensure that code snippets remain intact.        
        """
        return self.ask_gpt(role, content)

    def edit_article(self, editor_file: str) -> str:
        print(f"Editing article {editor_file}")
        with open(editor_file, "r") as file:
            content = file.read()
            edited_content = self.generate_review(content)
            title = self.generate_title(edited_content)
            subtitle = self.generate_subtitle(edited_content)
            closing_statement = self.generate_closing_statement(edited_content)

            final_content = f"""
# {title}\n 
{subtitle}\n\n
{edited_content}\n\n
# Conclusion\n
{closing_statement}
                """

            splitted = editor_file.split(os.sep)
            if len(splitted) == 1:
                splitted = [".", splitted[0]]
            target = os.sep.join(splitted[0:-1]) + os.sep + f"reviews_{splitted[-1]}"
            with open(target, "w") as target_file:
                target_file.write(final_content)
                print(f"Saving edited article to {target}")
                return target


ChatGptEditor().edit_article(sys.argv[1])
