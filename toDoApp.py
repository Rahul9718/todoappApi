
from flask import Flask , jsonify , request , abort, make_response, url_for
#to import Flask and jsonify from flask we have to give this command
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


app = Flask(__name__)
app.config.update({
    "DEBUG": True
})

tasks = [
    {
        'id':1,
        'title':'Students name',
        'description' : 'What to study',
        'done':False
    },
    {
        'id':2,
        'title':'Learn to python',
        'description': 'Everyone has to learn',
        'done': False
    },
    {
        'id':3,
        'title':'Learn Flask',
        'description':'yeah we will do it',
        'done':False
    }

]

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    # isme task naam ka variable mei hume ek loop chalaya aur uske andar ek if condition lagayi jo kehti hai
    # for task in tasks:
        # if task[id] == task_id:
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id' : tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id']==task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task):
    print task
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/taskz', methods=['GET'])
def get_taskz():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


users = [
    {'usern': 'rahul','password': '123'},
    {'usern': 'shivam','password': '456'},
    {'usern': 'nitin','password': '789'}
 ]

@auth.get_password
def get_password(username):
    new_user = [user for user in users if username == user['usern']]
    if len(new_user) == 0:
        abort(404)
    return new_user[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'unauthorized access'}),401)

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks' : tasks})


@app.route('/todo/api/v1.0/tasks/signup', methods = ['POST'])
def add_user():
    if not request.json or not 'usern' in request.json:
        abort(400)
    add = {
        'usern': request.json['usern'],
        'password' : request.json['password']
    }
    users.append(add)
    return jsonify({"user":add}), 201

if __name__ == '__main__':
    app.run()