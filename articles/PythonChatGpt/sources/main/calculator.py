from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatGptCalculator:
    _role = "You are a calculator. You'll receive mathematical operations, and you'll respond with only the mathematical answer."
    _client = OpenAI()

    def calculate(self, query: str) -> float:
        completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self._role,
                },
                {"role": "user", "content": query},
            ],
        )
        return float(completion.choices[0].message.content)
