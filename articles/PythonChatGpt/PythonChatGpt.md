# Unlocking the Potential: A Guide to Using ChatGPT from Python

Ready to harness the power of ChatGPT from your Python code for fame and glory? Read on!

## Setup

First things first: use *venv*. Don't know how or why? Check out my article on the subject: [Effective Python Development: Harnessing the Power of Virtual Environments](https://medium.com/@quentin.astegiano/effective-python-development-harnessing-the-power-of-virtual-environments-c01308189d6c).

You will need to install some dependencies for your code to work:

```bash
pip install openai
pip install python-dotenv
```

`openai` is the Python library provided by OpenAI. `python-dotenv` will allow you to store your API Key outside of your code - you don't want to publish that on GitHub!

Once that's done, create an `.env` file. Add a key to store your token:

```yaml
OPENAI_API_KEY=[YOUR TOKEN]
```

If you don't have an API token yet, you'll need to create an account on [https://www.openai.com] and manage your key here: [https://platform.openai.com/api-keys]. Yes, you need to set up payment details and maybe add some money to your account, but using ChatGPT for a couple of requests won't cost you more than some pennies; it's pretty cheap.

*Important!* Add your `.env` file to your `.gitignore`!

## A Calculator Powered By ChatGPT

Let's build a simple and silly example:

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

Let's break it down:

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
```

To use ChatGPT, you need to include the OpenAI module. The OpenAI module needs to access your API key. By using `load_dotenv()`, you will load the content of your `.env` file.

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

Here, we send a message to ChatGPT. The role `system` tells ChatGPT who he is and how he is supposed to respond; the role `user` is the query that will be sent.

```python
return float(completion.choices[0].message.content)
```

ChatGPT's response is in an easily accessible object. It might contain multiple answers; here we just get the content from the message of the first choice.

# Let's Test The Calculator

To test the calculator, I'm going to use *pytest*. Don't know how to use *pytest*? Refer to my other article on the subject: [Simple and Powerful Unit Testing in Python with Pytest](https://medium.com/@quentin.astegiano/simple-and-powerful-unit-testing-in-python-with-pytest-1f33f3cade15).

```python
class TestChatGptCalculator:
    @pytest.fixture
    def calculator(self) -> ChatGptCalculator:
        return ChatGptCalculator()

    def test_calculator_should_do_additions(self, calculator: ChatGptCalculator):
        assert calculator.calculate("3+5") == 8.0

    def test_calculator_should_do_subtractions(self, calculator: ChatGptCalculator):
        assert calculator.calculate("12 - 3") == 9.0

    def test_calculator_should_do_multiplications(self, calculator: ChatGptCalculator):
        assert calculator.calculate("8 * 4") == 32.0
```

And there you have it! The world's most inefficient calculator, subject to hallucinations, and prone to breaking!

# What's next?

The point of that article is not to present a usable case for ChatGPT but merely to demonstrate how one can call the OpenAI tool. In the future, we'll explore more complex and actionable integrations.

If you want to know more, I strongly suggest referring to the official documentation:

* The OpenAI documentation: [https://platform.openai.com/docs/quickstart?context=python]
* The Python library: [https://github.com/openai/openai-python]
