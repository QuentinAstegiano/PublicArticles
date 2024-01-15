# Why should we want to do that ?

Editing article is an actual skill.
Having a professional editor is a big help for writers.
When you don't have one, why not enlist the help of ChatGPT ? It'll be less efficient than an actual, real editor, but it'll be better than nothing

Let's try to write a Python program that'll use ChatGPT to edit my articles.

# Prerequisites

A ChatGPT API token
A Python 3 env

Don't know how to setup your environnement ? Check my guide : (Unlocking the Potential: A Guide to Using ChatGPT from Python)[https://medium.com/@quentin.astegiano/unlocking-the-potential-a-guide-to-using-chatgpt-from-python-1884fd7c3d7b]

# Building the bot

## Generating the actual reviewed article

We'll need to call ChatGPT multiple times to do multiple tasks, so let's start by creating a function to do a simple call and get the result.
The complete Python script is available on GitHub (link below).

Nothing fancy here : it's very similar to what was already showcased on my other article.

```python
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
```

First thing to do : the actual edition.
As always what matter the most is the prompt.

The idea here is to load the content of the file that we want to edit, and send it to ChatGPT for edition, and then get the restult back.
I'm asking ChatGPT to correct my mistakes, to enhance clarity, to reformulate... like an actual editor would do.

```python 
    def generate_review(self, content: str) -> str:
        print("Generating editor review...")
        role = """
            You are a skilled editor specialized in technical articles published on the internet.
            Review the provided article, correct any writing mistakes, and reformulate when necessary— even if it involves rewriting entire sentences. Create actual sentences when they are missing.
            Aim to enhance clarity, improve grammar, and refine the overall writing quality.
            Also aim to maximize reader engagement throughout the article.

            Ensure that code snippets remain intact.        
        """
        return self.ask_gpt(role, content)
```

What ChatGPT will produce probably won't be usable as is ; but it'll be a great staple to build upon.


But why stop here ? ChatGPT can do more than just editing. Why not also generate some additional content for our article, like a title, an introduction, or a closing statement ?

So let's write some other functions to enlist some more chatgpt help.

## Generating a title 

All those functions will work in the same way : make a prompt to ask ChatGPT something - here, a good title - and send the article content.

```python 
    def generate_title(self, content: str) -> str:
        print("Generating title...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            Write the best possible title for that article, to grab a reader attention and to maximize engagement.
        """
```

## Generating a subtitle / an introduction

The prompts listed here are quite simples, but it's possible to be a lot more fancy.
Actual constraints can (and should) be added - for example, about the size of the intro, or about the overall aim of the generated content.

```python 
    def generate_subtitle(self, content: str) -> str:
        print("Generating subtitle...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            Propose a great introduction to the following article, that would grab a reader attention.
            The introduction must be less than 200 characters long.
        """
        return self.ask_gpt(role, content)
```

## Generating a closing statement 

The last thing I'll want to generate here is a conclusion, to summarize what was written, and to open up the possibilities.
All those prompts are (a bit) tailored for technical articles ; you should definitely create some that work well with what you're writting.

```python 
    def generate_closing_statement(self, content: str) -> str:
        print("Generating closing statement...")
        role = """
            You are a skilled editor specialized on technical articles published on the internet.
            Write a suitable conclusion for the given article, sumarizing what was written and offering perspective on some next steps.
        """
        return self.ask_gpt(role, content)
```

## Putting it all together

The only thing left to do is to call all of our functions and to generate a complete text from it.

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

By calling that function with a path to your article file, it'll create new file located next to your article, prefixed by *review_*, containing the edited article.

```bash 
$ python3 sources/main/editor.py ./PythonChatGptMediumEditor.md
Editing article ./PythonChatGptMediumEditor.md
Generating editor review...
Generating title...
Generating subtitle...
Generating closing statement...
Saving edited article to ./reviews_PythonChatGptMediumEditor.md
```

For demonstration purpose, I've used that very script on that very article. 
You can see the original, unedited file here : 
And the edited version here : 


The complete source code is available on Github : link to Github
