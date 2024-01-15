from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatGptCalculator:
    _client = OpenAI()

    def calculate(self, query: str) -> float:
        completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a calculator. You'll receive mathematical operations, and you'll respond with only the mathematical answer.",
                },
                {"role": "user", "content": query},
            ],
        )
        return float(completion.choices[0].message.content)
