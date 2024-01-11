import pytest
from todolist import ToDoList, Task


# Tests for ToDoList class
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
