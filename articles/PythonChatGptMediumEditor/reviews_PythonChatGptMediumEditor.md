
#  "Unlocking the Power: Enhancing Technical Articles with ChatGPT Editor"
 
Introducing the Power of ChatGPT in Article Editing

Discover how to utilize ChatGPT to edit and enhance technical articles, even when a human editor is not available.


# Why


Editing an article is a genuine skill that can greatly benefit writers. While having a professional editor is ideal, sometimes it may not be feasible. In such cases, leveraging the assistance of ChatGPT can be a valuable alternative. While it may not be as efficient as a human editor, it is certainly better than having no editor at all.

Let's now proceed to write a Python program that utilizes ChatGPT to edit articles.

## Prerequisites

Before we begin, make sure you have the following:

- A ChatGPT API token
- Python 3 environment

If you are unsure of how to set up your environment, please refer to my guide: ["Unlocking the Potential: A Guide to Using ChatGPT from Python"](https://medium.com/@quentin.astegiano/unlocking-the-potential-a-guide-to-using-chatgpt-from-python)

## Building the bot

Since we will be using ChatGPT for multiple tasks, it is best to start by creating a function that performs a single unit call and returns the result.

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

Now, let's focus on the actual editing process. As always, the prompt is of utmost importance.

```python 
    def generate_review(self, content: str) -> str:
        print("Generating editor review...")
        role = """
            You are a skilled editor specialized in technical articles published on the internet.
            Your task is to review the provided article, correcting any writing mistakes and reformulating it when necessary. Feel free to rewrite entire sentences and add missing sentences as needed.
            Your goal is to enhance clarity, improve grammar, and refine the overall writing quality. Additionally, aim to maximize reader engagement throughout the article.

            Please ensure that code snippets remain intact.        
        """
        return self.ask_gpt(role, content)
```

But why stop there? Let's create additional functions to further utilize ChatGPT for assistance.

Generating a title: 
```python 
    def generate_title(self, content: str) -> str:
        print("Generating title...")
        role = """
            You are a skilled editor specialized in technical articles published on the internet.
            Your task is to write the best possible title for the article in order to capture the reader's attention and maximize engagement.
        """
```

Generating a subtitle/introduction:
```python 
    def generate_subtitle(self, content: str) -> str:
        print("Generating subtitle...")
        role = """
            You are a skilled editor specialized in technical articles published on the internet.
            Your task is to propose a compelling introduction for the following article that will grab the reader's attention.
            The introduction should be no more than 200 characters in length.
        """
        return self.ask_gpt(role, content)
```

Generating a closing statement: 
```python 
    def generate_closing_statement(self, content: str) -> str:
        print("Generating closing statement...")
        role = """
            You are a skilled editor specialized in technical articles published on the internet.
            Your task is to write a suitable conclusion for the given article, summarizing its contents and offering perspectives on potential next steps.
        """
        return self.ask_gpt(role, content)
```

Now, let's bring it all together: 
```python 
    def edit_article(self, editor_file: str) -> str:
        print(f"Editing article: {editor_file}")
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
            target = os.sep.join(splitted[0:-1]) + os.sep + f"reviews_{splitted[-1]}"
            with open(target, "w") as target_file:
                target_file.write(final_content)
            return target
```

The complete source code is available on [Github](link to Github).


# Conclusion

## Conclusion

In this article, we explored the use of ChatGPT as a tool for editing technical articles. We discussed the benefits of having a professional editor and acknowledged that utilizing ChatGPT can be a valuable alternative when human editing is not feasible.

We provided a step-by-step guide on how to build a Python program that leverages the ChatGPT API for editing articles. We demonstrated how to generate an editor review, title, subtitle/introduction, and closing statement using ChatGPT.

By incorporating ChatGPT into the editing process, we can enhance the clarity, improve grammar, and refine the overall writing quality of technical articles. Additionally, we can maximize reader engagement and ensure that code snippets remain intact.

Moving forward, it would be beneficial to continue refining and optimizing the editing functions. Exploring different prompt strategies and fine-tuning the model's responses can help achieve even better results. Furthermore, considering the integration of other AI tools for specific editing tasks, such as code analysis and plagiarism detection, can further enhance the editing process.

In conclusion, leveraging the power of ChatGPT can empower writers and editors alike to produce high-quality technical articles that captivate readers and offer valuable insights.
                