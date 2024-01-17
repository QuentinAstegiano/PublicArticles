from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

from mistralai.client import MistralClient

client = MistralClient()
response = client.chat(
    model="mistral-tiny",
    messages=[ChatMessage(role="user", content="What is MistralAI ?")],
)

print(response.choices[0].message.content)
