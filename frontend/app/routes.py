from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for
)

import requests

app = Flask(__name__)
BACKEND_URL = 'http://localhost:5000/tasks'

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/about')
def about():
    return render_template('about.html')

@app.get('/tasks')
def task_list():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get('tasks')
        return render_template('list.html',tasks=task_list)
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )

@app.get('/tasks/<int:pk>')
def detail(pk):
    url = "%s/%s" % (BACKEND_URL,pk)
    response = requests.get(url)
    if response.status_code == 200:
        task = response.json().get('task')
        return render_template('detail.html',task=task)
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )

@app.get('/create')
def create():
    return render_template('new.html')

@app.post('/create')
def new_task():
    name = request.form['name']
    summary = request.form['summary']
    description = request.form['description']
    data = {
        'name': name,
        'summary': summary,
        'description': description
    }
    response = requests.post(BACKEND_URL, json=data)
    print(response.text)
    if response.status_code == 204:
        return redirect(url_for('new_task'))
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )

@app.get('/tasks/edit')
def edit():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get('tasks')
        return render_template('edit.html',tasks=task_list)
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )

@app.post('/tasks/<int:pk>')
def update(pk):
    url = "%s/%s" % (BACKEND_URL,pk)
    name = request.form['name']
    summary = request.form['summary']
    description = request.form['description']
    data = {
        'name': name,
        'summary': summary,
        'description': description
    }
    response = requests.put(url, json=data)
    if response.status_code == 204:
        return redirect(url_for('task_list'))
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )