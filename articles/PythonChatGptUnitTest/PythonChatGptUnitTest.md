# Generating unit tests with ChatGpt

ChatGPT can be used for a lot of things. Why not ask it to write some tests for us ?

## Why

Writing tests is essential.
Writing them all by hand can be long and cumbersome. What if we can ask our favorite bot for some tests, to jump start our activity ?

## Prerequisite

The idea here is to call ChatGPT with a prompt asking it to write some unit test, provide it with the source code, and write the result to a test file.

I won't cover here the details of ChatGPT integration in Python ; if you need a refresher, read my other article : (Unlocking the Potential: A Guide to Using ChatGPT from Python)[https://medium.com/@quentin.astegiano/unlocking-the-potential-a-guide-to-using-chatgpt-from-python-1884fd7c3d7b]

## Building The Test Generator

Let's dive into the specifics.
Here's the code to call ChatGPT.

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

As usual, you give a role to ChatGPT, here one of an "expert Python developper" ; provide him as a user of the required data ; and process it's response.

To get the content, we'll take a file name, and load its content :
```python
  def get_file_content(self, source: str) -> str:
    with open(source, "r") as file:
      content = file.read()
      return content
  def generate(self, source: str) -> str:
    content = self.get_file_content(source)
    return self.call_gpt(content)
```

The only thing to do is to write the result to a test file - here I choose to prefix the class by "test_" and to put it next to the source code.
```python
  def create_test_file(self, source: str) -> str:
    content = self.generate(source)
    splitted = source.split(os.sep)
    target = os.sep.join(splitted[0:-1]) + os.sep + f"test_{splitted[-1]}"
    with open(target, "w") as file:
      file.write(content)
    return target
```

That litteraly all that is necessary for this task - albeit with a simplistic implementation.

The complete source code is available on GitHub : 

## Testing The Generator

Let's apply this generator to an example class, say, a simplistic implementation of a todolist : 

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

I'll create a simple *main* class to call the generator with a given parameter : 
```python
from test_generator import TestGenerator
import sys

source_file = sys.argv[1]
print(f"Generating test file for {source_file}")

test_file = TestGenerator().create_test_file(source_file)
print(f"Test file generated : {test_file}")
```

Let's run it.

```bash
$ python source/main/start_generator.py source/main/todolist.py
Generating test file for source/main/todolist.py
Test file generated : source/main/test_todolist.py
```

And indeed, we got some tests !

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

So, we used ChatGPT to generate some tests.
Are those tests helpful ? Yes. Are they great ? No.

ChatGPT can do much more than that, and provide test that are of much higher quality.
The issue here is the prompt used. It's very simple, doesn't provide any guideline nor examples.

ChatGPT can only be as good as the questions we ask it. 
Using the example provided here, you can try some more appropriate prompts to get even better results !
