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

@app.get('/tasks/<msg>')
def success(msg):
    return render_template('success.html',msg=msg)

@app.post('/tasks/<int:pk>')
def update(pk):
    print('update')
    url = "%s/%s" % (BACKEND_URL,pk)
    method = request.form['_method']
    if method == 'DELETE':
        print('delete')
        response = requests.delete(url)
        if response.status_code == 204:
            return redirect(url_for('success', msg='Task deleted successfully'))
        return(
            render_template('error.html',err=response.status_code),
            response.status_code
        )
    elif method == 'PUT':
        name = request.form['name']
        summary = request.form['summary']
        description = request.form['description']
        state = request.form['state']
        if state == 'True':
            state = True
        else:
            state = False
        data = {
            'name': name,
            'summary': summary,
            'description': description,
            'is_done': state
        }
        response = requests.put(url, json=data)
        if response.status_code == 204:
            return redirect(url_for('success', msg='Task updated successfully'))
        return(
            render_template('error.html',err=response.status_code),
            response.status_code
        )

@app.delete('/tasks/<int:pk>')
def delete(pk):
    url = "%s/%s" % (BACKEND_URL,pk)
    response = requests.delete(url)
    if response.status_code == 204:
        return redirect(url_for('success', msg='Task deleted successfully'))
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )

'''
@app.get('tasks/edit'/<int:pk>)
def edit(pk):
    url = "%s/%s" % (BACKEND_URL,pk)
    response = requests.get(url)
    if response.status_code == 200:
        task = response.json().get('task')
        return render_template('edit.html',task=task)
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )
@app.post('tasks/edit'/<int:pk>)
def submit_task_update(pk):
    url = "%s/%s" % (BACKEND_URL,pk)
    task_data =request.form
    response = requests.put("success.html", msg="Task updated successfully")
    if response.status_code == 204:
        return redirect(url_for('task_list'))
    return(
        render_template('error.html',err=response.status_code),
        response.status_code
    )
'''
