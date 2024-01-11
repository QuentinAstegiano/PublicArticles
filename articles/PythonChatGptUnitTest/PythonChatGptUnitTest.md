# Streamlining Test Generation: Harnessing ChatGPT's Power for Automated Unit Tests in Python

ChatGPT is a versatile tool with the capability to assist in various tasks. How about leveraging its potential to automate the generation of unit tests?

## Why Use ChatGPT for Unit Tests?

Writing unit tests is a crucial aspect of software development. However, the manual creation of extensive test suites can be time-consuming and tedious. Imagine if you could expedite this process by enlisting the help of your favorite AI bot – ChatGPT.

## Prerequisite

For a quick refresher on how to integrate ChatGPT in any Python program, you can refer to my previous article: (Unlocking the Potential: A Guide to Using ChatGPT from Python)[https://medium.com/@quentin.astegiano/unlocking-the-potential-a-guide-to-using-chatgpt-from-python-1884fd7c3d7b]

## Building The Test Generator

Let's explore the specific implementation. The following code snippet demonstrates how to call ChatGPT:

``` python
  def call_gpt(self, content: str) -> str:
    completion = self._client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": """
            You're an expert Python developper, who can use the pytest library to write useful and meaningful tests in python.
            Write the tests for this file. Output only the tests, and no textual explanations. Comments are allowed, if necessary.""",
        },
        {"role": "user", "content": content},
      ],
    )
    return completion.choices[0].message.content
```

In this code, ChatGPT is assigned the role of an "expert Python developer." The user provides the required data, and the response is processed accordingly.

To obtain the content for processing, a file name is taken, and its content is loaded:

```python
  def get_file_content(self, source: str) -> str:
    with open(source, "r") as file:
      content = file.read()
      return content
  def generate(self, source: str) -> str:
    content = self.get_file_content(source)
    return self.call_gpt(content)
```

The result is then written to a test file, with a naming convention of prefixing "test_" to the class and placing it next to the source code:

```python
  def create_test_file(self, source: str) -> str:
    content = self.generate(source)
    splitted = source.split(os.sep)
    target = os.sep.join(splitted[0:-1]) + os.sep + f"test_{splitted[-1]}"
    with open(target, "w") as file:
      file.write(content)
    return target
```

This simple implementation covers the essential steps for the task.
The complete source code is accessible on (GitHub)[https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/PythonChatGptUnitTest/sources/main/test_generator.py]

## Testing The Generator

Let's apply the generator to an example class – a basic implementation of a to-do list:

```python
from dataclasses import dataclass
from typing import Dict
import uuid


@dataclass
class Task:
  id: int
  title: str
  content: str
  done: bool


class ToDoList:
  _tasks: Dict[int, Task] = {}

  def new_task(self, title: str, content: str) -> Task:
    task = Task(id=uuid.uuid4().int, title=title, content=content, done=False)
    self._tasks[task.id] = task
    return task

  def mark_as_done(self, id):
    if id not in self._tasks:
      raise TypeError()
    else:
      self._tasks[id].done = True

  def get_all_tasks(self):
    return self._tasks.values()
```

To invoke the generator, create a simple main class:


```python
from test_generator import TestGenerator
import sys

source_file = sys.argv[1]
print(f"Generating test file for {source_file}")

test_file = TestGenerator().create_test_file(source_file)
print(f"Test file generated : {test_file}")
```

Execute the script with the desired source file:

```bash
$ python source/main/start_generator.py source/main/todolist.py
Generating test file for source/main/todolist.py
Test file generated : source/main/test_todolist.py
```

Indeed, the tests have been successfully generated:

```python
def test_new_task():
  todo_list = ToDoList()
  task = todo_list.new_task("Title", "Content")
  assert isinstance(task, Task)
  assert task.title == "Title"
  assert task.content == "Content"
  assert not task.done


def test_mark_as_done():
  todo_list = ToDoList()
  task = todo_list.new_task("Title", "Content")
  todo_list.mark_as_done(task.id)
  assert task.done


def test_mark_as_done_with_invalid_id():
  todo_list = ToDoList()
  with pytest.raises(TypeError):
    todo_list.mark_as_done(123)


def test_get_all_tasks():
  todo_list = ToDoList()
  task1 = todo_list.new_task("Title1", "Content1")
  task2 = todo_list.new_task("Title2", "Content2")
  all_tasks = todo_list.get_all_tasks()
  assert task1 in all_tasks
  assert task2 in all_tasks
```

## Closing Words

By utilizing ChatGPT, we've automated the test generation process.
Are these tests helpful? Yes. Are they optimal? No.

The quality of the generated tests depends on the prompt used. The example prompt here is simplistic, lacking guidelines and examples.
Remember, ChatGPT's effectiveness relies on the questions we pose. Experiment with more detailed and precise prompts to obtain even better results!
