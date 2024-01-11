# Using Chat GPT from Python

Ready to harness the power of ChatGpt from your python code, for fame and glory ? Read on !

## Setup

First thing first : use *venv*. Don't know how or why ? Check my article on the subject : [Effective Python Development: Harnessing the Power of Virtual Environments](https://medium.com/@quentin.astegiano/effective-python-development-harnessing-the-power-of-virtual-environments-c01308189d6c)

You will need to install some dependencies for your code to work :
```bash
pip install openai
pip install python-dotenv
```

`openai` is the python library provided by OpenAI. 
`python-dotenv` will allow you to store your API Key outside of your code - you don't want to publish that on github !

Once that done, create an `.env` file.
Add a key to store your token : 
```yaml
OPENAI_API_KEY=[YOUR TOKEN]
```

If you don't have an API token yet, you'll need to go to create an account on [https://www.openai.com], and manage your key here : [https://platform.openai.com/api-keys]
Yes, you need to setup payment details, and maybe add some money to your account ; but using ChatGpt for a couple request won't cost you more than some pennies, it's pretty cheap.

*Important !*
Add your *.env* file to your *.gitignore* !

## A Calculator Powered By ChatGpt

Let's build a simple and silly example : 

```python 
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
                    "content": "You are a calculator. You'll receive mathematical operations, and you'll respond with only the mathematical answer."
                },
                {"role": "user", "content": query},
            ],
        )
        return float(completion.choices[0].message.content)
```

Let's break it down :

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
```

To use ChatGpt, you need to include the OpenAI module.
The OpenAI module need to access your API key. By using `load_dotenv()` you will load the content of your `.env` file.


```python 
        completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a calculator. You'll receive mathematical operations, and you'll respond with only the mathematical answer."
                },
                {"role": "user", "content": query},
            ],
        )
```

Here, we send a message to ChatGpt. The role `system` tell ChatGpt who he is, and how he is supposed to respond ; the role `user` is the query that will be sent.

```python
completion.choices[0].message.content
```

ChatGpt response is in an easily accessible object. It might contains multiple answers ; here we just get the content from the message of the first choice.

# Let's Test The Calculator

To test the calculator, I'm going to use *pytest*.
Don't know how to use *pytest* ? Refer to my other article on the subject : [Simple and Powerful Unit Testing in Python with Pytest](https://medium.com/@quentin.astegiano/simple-and-powerful-unit-testing-in-python-with-pytest-1f33f3cade15)

```python
class TestChatGptCalculator:
    @pytest.fixture
    def calculator(self) -> ChatGptCalculator:
        return ChatGptCalculator()

    def test_calculator_should_do_additions(self, calculator: ChatGptCalculator):
        assert calculator.calculate("3+5") == 8.0

    def test_calculator_should_do_substractions(self, calculator: ChatGptCalculator):
        assert calculator.calculate("12 - 3") == 9.0

    def test_calculator_should_do_multiplications(self, calculator: ChatGptCalculator):
        assert calculator.calculate("8 * 4") == 32.0
```

And there you have it ! The world most ineficient calculator, subject to hallucinations, and prone to breaking !

# What's next ?

The point of that article is not to present a usable case for ChatGpt, but merely to demonstrate how one can call the OpenAI tool.
In the future, we'll explore more complex and actionnable integrations.

If you want to know more, I strongly suggest to refer to the official documentation : 
* The OpenAI documentation : [https://platform.openai.com/docs/quickstart?context=python]
* The python lib : [https://github.com/openai/openai-python]
