#!/usr/bin/env python3

import typer
from loguru import logger
from rich.console import Console
from rich.table import Table

from database import (complete_todo, delete_todo, get_all_todos, insert_todo,
                      update_todo)
from model import Todo

logger.add(
    "log/todocli.log",
    format="{time}, {level}, {message}",
    level="INFO",
    rotation="00:00",
    compression="zip",
)

console = Console()

app = typer.Typer()


@logger.catch
@app.command(short_help="adds an item")
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()


@logger.catch
@app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_todo(position - 1)
    show()


@logger.catch
@app.command()
def update(position: int, task: str = None, category: str = None):
    typer.echo(f"updating {position}")
    update_todo(position - 1, task, category)
    show()


@logger.catch
@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_todo(position - 1)
    show()


@logger.catch
@app.command()
def show():
    tasks = get_all_todos()
    console.print("[bold yellow]Todos[/bold yellow]:", "\uf4a0")

    table = Table(show_header=True, header_style="bold green")
    table.add_column("#", style="dim", width=6)
    table.add_column("ToDo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        colors = {
            "GitHub": "yellow",
            "Learn": "cyan",
            "Python": "purple",
            "Sport": "cornflower_blue",
            "Study": "green",
            "Work": "blue",
            "YouTube": "red",
        }
        if category in colors:
            return colors[category]
        return "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "\ueab2" if task.status == 2 else "\ueab8"
        table.add_row(
            str(idx),
            task.task,
            f"[{c}]{task.category}[/{c}]",
            is_done_str)
    console.print(table)


if __name__ == "__main__":
    app()
