# pip install "fastapi[all]" jinja2

from typing import Annotated, TypedDict

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


class Task(TypedDict):
    id: str
    title: str
    is_done: bool


app = FastAPI()

tasks: list[Task] = []


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"tasks": tasks}
    )


@app.post("/create", response_class=HTMLResponse)
async def create(request: Request, task: Annotated[str, Form()]):
    tasks.append({"id": len(tasks), "title": task, "is_done": False})

    return templates.TemplateResponse(
        request=request, name="tasks.html", context={"tasks": tasks}
    )


@app.post("/update", response_class=HTMLResponse)
async def update(
    request: Request, id: Annotated[int, Form()], is_done: Annotated[bool, Form()]
):
    tasks[id]["is_done"] = is_done

    return templates.TemplateResponse(
        request=request, name="tasks.html", context={"tasks": tasks}
    )


@app.post("/clean", response_class=HTMLResponse)
async def clean(request: Request):
    tasks.clear()

    return templates.TemplateResponse(
        request=request, name="tasks.html", context={"tasks": tasks}
    )
