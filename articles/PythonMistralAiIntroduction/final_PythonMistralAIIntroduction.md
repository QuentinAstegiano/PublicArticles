
# Forget about ChatGPT, Discover MistralAI : the forefront of the AI revolution
 
Discover MistralAI: a revolutionary language model offering human-like text generation, deep understanding, and creativity. Start your journey with this new hot language model right now !

# Introduction

MistralAI is a cutting-edge large language model (LLM) developed by a French start-up, designed to rival industry giants like ChatGPT. 
It's creating great content, it's cheap, it's easy to use... what's not to like ?

To show you some of this engine capabilities, I'll guide you through you through the process of utilizing MistralAI to build a Medium Article Editor, similar to the one I have created here with ChatGPT: [Unlocking the Power of ChatGPT: Revolutionize Your Technical Article Editing](https://medium.com/@quentin.astegiano/unlocking-the-power-of-chatgpt-revolutionize-your-technical-article-editing-d6ae637698ba).

# Getting Started with MistralAI

To get started with MistralAI, you need an API key, which you can obtain by signing up on their [website](https://mistral.ai/). The pricing is based on token usage and is quite affordable: [MistralAI Pricing](https://docs.mistral.ai/platform/pricing/). A standard round trip will typically use a couple hundred tokens at most, with the cheapest model costing €0.14 per million input tokens and €0.42 per million output tokens. Additionally, you can set a usage limit (e.g., €5 or €10 per month) to prevent overspending.

For this example, we will use Python. Ensure you have Python 3 installed and set up a virtual environment with the following libraries:

```bash
pip install mistralai 
pip install python-dotenv
```

Create a `.env` file and insert your secret API key:

```ini
MISTRAL_API_KEY=[YOUR_API_KEY]
```

# Verifying the MistralAI Installation

To ensure everything is working as intended, make a initial call to MistralAI:

```python
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
```

This code snippet loads the environment, creates a client, and asks a simple question to the model. Note that the `load_dotenv()` function must be called before importing the `MistralClient` for the client to access your API key properly.

# Building a Medium Article Editor with MistralAI

The complete source code is available on my [GitHub](https://github.com/quentin-astegiano/mistral-medium-article-editor).

Start by creating a class to manage the entire process:

```python
from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

from mistralai.client import MistralClient

class MistralEditor:
  _client = MistralClient()
```

As previously, the `MistralClient` needs to be imported after the `load_dotenv()` call to access the API key correctly.

To simplify the process, create a function to handle the actual call to Mistral:

```python
  def ask_mistral(self, system_role: str, query: str) -> str:
    completion = self._client.chat(
      model="mistral-small",
      messages=[
        ChatMessage(role="system", content=system_role),
        ChatMessage(role="user", content=query),
      ],
    )
    return completion.choices[0].message.content
```

Now, use Mistral to perform various tasks, such as creating a title or correcting text:

```python
  def generate_title(self, content: str) -> str:
    print("Generating title...")
    role = """
      You are a skilled editor specialized in technical articles published on the internet.
      Write the best possible title for that article, to grab a reader's attention and to maximize engagement.
      The title must be less than 120 characters long.
    """
    title = self.ask_mistral(role, content)
    if title.startswith("#"):
      title = title.replace("#", "")
    return title

  def generate_review(self, content: str) -> str:
    print("Generating editor review...")
    role = """
      You are a skilled editor specialized in technical articles published on the internet.
      Review the provided article, correct any writing mistakes, and rephrase when necessary—even if it involves rewriting entire sentences. Create actual sentences when they are missing.
      Aim to enhance clarity, improve grammar, and refine the overall writing quality.
      Also aim to maximize reader engagement throughout the article. The sections titles can also be rewritten when appropriate.
      When possible, generate additional content to expand on what is written in the article, without changing the original meaning.
      Try not to remove content from the original article; reformulate when necessary, but keep at least the meaning of what was written.

      Ensure that code snippets remain intact.
    """
    return self.ask_mistral(role, content)
```

Finally, load the content file, call the Mistral functions, and create the results based on the outputs:

```python
  def edit_article(self, editor_file: str) -> str:
    print(f"Editing article {editor_file}")
    with open(editor_file, "r") as file:
      content = file.read()
      edited_content = self.generate_review(content)
      title = self.generate_title(edited_content)
      subtitle = self.generate_subtitle(edited_content)
      closing_statement = self.generate_closing_statement(edited_content)

      final_content = f"""
# {title}\n\
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
```

With this MistralAI-powered Medium editor, you can review your articles, correct mistakes, and enhance your writing.

Example usage:

```bash
$ python3 sources/main/editor.py PythonMistralAIIntroduction.md
Editing article PythonMistralAIIntroduction.md
Generating editor review...
Generating title...
Generating subtitle...
Generating closing statement...
Saving edited article to ./reviews_PythonMistralAIIntroduction.md
```

# Conclusion

MistralAI is an incredible tool with excellent capabilities. It's at the very forefront of the AI revolution.

The usage presented here is merely a toy (albeit an useful one, at least to correct my spelling mistakes...).

The content created by MistralAI is excellent, and it's ability to understand written language is impressive.
I'll explore some more complex and useful use of MistralAI in some future articles.
