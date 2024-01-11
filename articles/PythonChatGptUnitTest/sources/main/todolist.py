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
