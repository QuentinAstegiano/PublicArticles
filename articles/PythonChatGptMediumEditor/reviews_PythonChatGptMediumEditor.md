
#  Amplify Your Article's Impact: Unlocking the Power of a Technical Editor
 
## Unleashing the Power of ChatGPT: An Editor for Your Articles

Discover how ChatGPT can enhance your writing as a handy editor. Learn how to utilize the ChatGPT API to generate a revised version of your articles and even create captivating titles and introductions.


# Why Should We Use an Editor for Our Articles?

Editing an article is a valuable skill that can greatly benefit writers. While having a professional editor is ideal, if one is not available, there is still an option to enlist the help of ChatGPT. Though not as efficient as a human editor, ChatGPT can provide valuable feedback and revisions to improve the overall quality of the article.

To demonstrate how ChatGPT can be used as an editor, we will build a Python program that utilizes the ChatGPT API. Before we begin, make sure you have a ChatGPT API token and a Python 3 environment. If you need help with the setup process, please refer to my guide: "Unlocking the Potential: A Guide to Using ChatGPT from Python."

## Building the Bot

The first step in utilizing ChatGPT as an editor is to generate a reviewed version of the article. To do this, we will call ChatGPT multiple times for different tasks. Let's start by creating a function that makes a simple API call to get the result:

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

Next, we will write a function to generate the editor's review. We load the content of the file we want to edit, send it to ChatGPT, and receive the revised version. We instruct ChatGPT to correct mistakes, enhance clarity, and create actual sentences when needed—similar to what a human editor would do:

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

The output we receive might not be directly usable, but it serves as a useful starting point for further refinement.

But why stop at editing? ChatGPT is capable of much more. Let's also use it to generate additional content for our article, such as a title, an introduction, and a closing statement. For each of these tasks, we will create similar functions where we make a prompt to ask ChatGPT for help:

```python
def generate_title(self, content: str) -> str:
    print("Generating title...")
    role = """
        You are a skilled editor specialized in technical articles published on the internet.
        Write the best possible title for this article to grab the reader's attention and maximize engagement.
    """
    return self.ask_gpt(role, content)
```

```python
def generate_subtitle(self, content: str) -> str:
    print("Generating subtitle...")
    role = """
        You are a skilled editor specialized in technical articles published on the internet.
        Propose a compelling introduction to this article that would capture the reader's attention.
        The introduction should be less than 200 characters long.
    """
    return self.ask_gpt(role, content)
```

```python
def generate_closing_statement(self, content: str) -> str:
    print("Generating closing statement...")
    role = """
        You are a skilled editor specialized in technical articles published on the internet.
        Write a suitable conclusion for this article, summarizing the main points and offering perspectives on next steps.
    """
    return self.ask_gpt(role, content)
```

With all these individual functions in place, we can now put them together to generate a complete edited version of the article:

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

By calling this function with the path to your article file, it will generate a new file prefixed with "review_" containing the edited version of the article. For example:

```bash
$ python3 sources/main/editor.py ./PythonChatGptMediumEditor.md
Editing article ./PythonChatGptMediumEditor.md
Generating editor review...
Generating title...
Generating subtitle...
Generating closing statement...
Saving edited article to ./reviews_PythonChatGptMediumEditor.md
```

For demonstration purposes, I have used this script on the current article itself. You can find the original, unedited file [here](https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/PythonChatGptMediumEditor/PythonChatGptMediumEditor.md) and the edited version [here](https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/PythonChatGptMediumEditor/reviews_PythonChatGptMediumEditor.md).

The complete source code is available on [GitHub](https://github.com/QuentinAstegiano/PublicArticles/tree/main/articles/PythonChatGptMediumEditor).


# Conclusion

In conclusion, utilizing an editor for our articles, whether it be a professional human editor or a tool like ChatGPT, is crucial for enhancing the overall quality of our writing. In this article, we demonstrated how ChatGPT can be used as an editor by building a Python program that leverages the ChatGPT API.

We started by creating a function that makes API calls to ChatGPT to get the edited version of the article. This function instructs ChatGPT to correct mistakes, improve clarity, and create complete sentences. We then explored how ChatGPT can go beyond editing and be used to generate additional content like titles, subtitles, and closing statements for our article.

By combining these individual functions, we were able to generate a complete edited version of the article. This process was exemplified using a Python program that takes the path to an article file as input and outputs a new file with the edited version.

While ChatGPT may not be as efficient as a human editor, it still provides valuable feedback and revisions to enhance the quality of our articles. It serves as a useful starting point for further refinement by human editors.

As we continue to explore the potential of AI in editing, it is important to remember that it should complement, rather than replace, human editors. Human expertise is essential in maintaining the nuances of language, understanding context, and ensuring the overall coherence of the article.

In the future, we can expect AI editing tools like ChatGPT to become more advanced and offer even more sophisticated editing capabilities. This can lead to increased efficiency and improved accuracy in the editing process.

So, whether we have access to a human editor or rely on AI editing tools like ChatGPT, the goal remains the same—to produce high-quality articles that engage readers and effectively communicate complex technical topics. The combination of human expertise and AI assistance holds great potential in achieving this goal.
                