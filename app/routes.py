from flask import (
    Flask,
    render_template,
    request as req                  # given this an alias; the Request context object
)

import requests                         # this is the standalone request python package 

BACKEND_URL ="http://127.0.0.1:5000/tasks"

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/tasks")
def view_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )


@app.get("/tasks/<int:pk>/")
def single_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("detail.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/new/")
def new_form():
    return render_template("new.html")

@app.post("/tasks/new/")
def create_task():
    task_data =req.form
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", message="Tasj created")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/edit/")        # idea behind this is to pre-populate the form 
def edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit/")
def update_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.put(url, json=req.json)
    if response.status_code == 204:
        return render_template("success.html", message="Task edited")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )


@app.get("/tasks/<int:pk>/delete/")
def delete_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data =response.json().get("task")
        return render_template("delete.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/delete/")
def delete_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)
    if response.status_code == 204:
        return render_template("success.html", message="Task deleted")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )