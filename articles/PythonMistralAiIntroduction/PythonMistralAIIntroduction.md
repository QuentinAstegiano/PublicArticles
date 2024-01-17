# What is MistralAI ?

(MistralAI)[https://mistral.ai/] is a recent LLM created by a French start-up. It's positionned as a rival to ChatGPT, and... it's absolutly great.
It's powerful, it's easy to use, it's quick, it's cheap. It's a great model built for being able to process large and complex texts.

To showcase what can be done with it, and how to use it, I'll explain here how to use MistralAI to build a Medium Article Editor, similar to the one I posted here : [https://medium.com/@quentin.astegiano/unlocking-the-power-of-chatgpt-revolutionize-your-technical-article-editing-d6ae637698ba]

# The basics

To use MistralAI, you'll need an API Key, which you can get by signing up on (their website)[https://mistral.ai/].
The pricing is based on token usage, and it's *really* cheap : [https://docs.mistral.ai/platform/pricing/] A standard round trip will be a couple hundred tokens at most, and the cheapest model comes at 0.14€ per *million* input token and 0.42€ per *million* output token. Oh, and you can set an usage limit (say, 5 or 10€ per month) if you really want to be sure not to overspend.

The example I'm going to build here will be done in Python, so you'll also need a Python 3 environnement.

Start by [setting up a virtual environnement](https://medium.com/@quentin.astegiano/effective-python-development-harnessing-the-power-of-virtual-environments-c01308189d6c) and pull the required library : 

```bash 
pip install mistralai 
pip install python-dotenv
```

Create a `.env` file and put your secret API key in it :

```ini
MISTRAL_API_KEY=[YOUR API KEY]
```

# Checking that everything is ok

Lets make a first call to MistralAI to ensure that everything work as intented.

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

Here we start by loading our environnement, creating a client, and using it to ask a first simple question to the model.
The model to use need to be specified.
*mistral-tiny* is the cheapest one, works only in english, and is said to have limited reasoning capabilities.
*mistral-small* supports also French, German, Italian and Spanish. It can produce and reason about code, and have more capabilities in general.

The others models are either not yet publicly avaible or not suited to our examples.

Note that `load_dotenv()` have to be called *before* importing the *MistralClient*. If you do it afterward, then the client won't be able to load your api key.

Apart from that, the python client looks a lot like the ChatGPT one.

Indeed, everything works : 
```bash
$ python sources/main/mistral.py
Mistral AI is a cutting-edge company based in Paris, France, developing large language models. I am delighted to be one of the models developed by Mistral AI. Our models are designed to understand and generate human-like text based on the input they receive. They can be used for various applications such as text generation, translation, summarization, and question.
```

# Let's build a Medium article editor !

The complete source code is available on my GitHub : [link to github]

The first step is to create a class to manage the whole process : 
```python
from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

from mistralai.client import MistralClient

class MistralEditor:
  _client = MistralClient()
```

As before, the *MistralClient* needs to be imported after the *load_dotenv()* call to properly access your api key.

As we'll need to do multiple calls to Mistral, I'll first create a small function to do the actual call : 

```python
  def ask_mistral(self, system_role: str, query: str) -> str:
    completion = self._client.chat(
      model="mistral-small",
      messages=[
        ChatMessage(role="system", content=system_role),
        ChatMessage(role="user", content=query),
      ],
    )
```
I choose to use *mistral-small* here instead of *mistral-tiny* to try to get some better content.

With that out of the way, we just need to ask Mistral to do whatever we want, like creating a title, or correcting the mistakes in the text : 
```python
  def generate_title(self, content: str) -> str:
    print("Generating title...")
    role = """
      You are a skilled editor specialized on technical articles published on the internet.
      Write the best possible title for that article, to grab a reader attention and to maximize engagement.
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
      Review the provided article, correct any writing mistakes, and reformulate when necessary— even if it involves rewriting entire sentences. Create actual sentences when they are missing.
      Aim to enhance clarity, improve grammar, and refine the overall writing quality.
      Also aim to maximize reader engagement throughout the article. The sections titles can also be rewritten when appropriate.
      When possible, generate additional content to expand on what is written in the article, without changing the original meaning.
      Try not to remove content from the original article ; reformulate when necessary, but keep at least the meaning of what was written.

      Ensure that code snippets remain intact.    
    """
    return self.ask_mistral(role, content)
```

The only thing left to do is standard Python : loading the content file, calling the mistral functions, and creating the results based on the outputs : 
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
```

And there you have it : a MistralAI powered Medium editor, capable of reviewing your articles, correcting your mistakes, helping you to write some better articles.

```bash
$ python3 sources/main/editor.py PythonMistralAIIntroduction.md
Editing article PythonMistralAIIntroduction.md
Generating editor review...
Generating title...
Generating subtitle...
Generating closing statement...
Saving edited article to ./reviews_PythonMistralAIIntroduction.md
```
