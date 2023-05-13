#!/usr/bin/env python3
import sqlite3
import datetime

from loguru import logger
from typing import List
from model import Todo

logger.add(
    "log/todo_database.log",
    format="{time}, {level}, {message}",
    level="INFO",
    rotation="00:00",
    compression="zip",
)

conn = sqlite3.connect('todos.db')
c = conn.cursor()

@logger.catch
def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )""")

create_table()

@logger.catch
def insert_todo(todo: Todo):
    c.execute('SELECT count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
        {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added, 'date_completed': todo.date_completed, 'status': todo.status, 'position': todo.position})

@logger.catch
def get_all_todos() -> List[Todo]:
    c.execute('SELECT * FROM todos')
    results = c.fetchall()
    todos =[]
    for result in results:
        todos.append(Todo(*result))
    return todos

@logger.catch
def delete_todo(position):
    c.execute('SELECT count(*) FROM todos')
    count = c.fetchone()[0]

    with conn:
        c.execute('DELETE FROM todos WHERE position=:position',
                {"position": position})

        for pos in range(position+1, count):
            change_position(pos, pos-1, False)

@logger.catch
def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
        {'position_old': old_position, 'position_new': new_position}
    )
    if commit:
        conn.commit()

@logger.catch
def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE todos SET task = :task, category = :category WHERE position = :position',
             {'position': position, 'task': task, 'category': category}
            )
        elif task is not None:
            c.execute('UPDATE todos SET task = :task WHERE position = :position',
                {'position': position, 'task': task}
            )
        elif category is not None:
            c.execute('UPDATE todos SET category = :category WHERE position = :position',
                {'position': position, 'category': category}
            )

@logger.catch
def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position',
            {'position': position, 'date_completed': datetime.datetime.now().isoformat()}
        )
