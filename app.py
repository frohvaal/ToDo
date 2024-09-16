import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usertodo:todo1234@localhost:3306/todo-mariadb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model): #Create the model of database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_created': self.date_created.isoformat(),
            'is_completed': self.is_completed
        }

# Route to get all task of ToDo App
@app.route('/todo', methods=['GET'])
def get_all_tasks():
    tasks = db.session.query(ToDo).all()
    return jsonify([task.to_dict() for task in tasks]), 200

#Route for get a specific To-Do by id
@app.route('/todo/<int:id>', methods=['GET'])
def get_task(id):
    task = db.session.get(ToDo, id)

    if task is None:
        # If task is not found, return a 404 error
        return abort(404, description="Task not found")
    
    return jsonify(task.to_dict()), 200  # Return the task en JSON format

# Route to create a new task
@app.route('/todo', methods=['POST'])
def create_task():
    data = request.json

    new_task = ToDo(
        title=data.get('title'),
        description=data.get('description'),
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Created"}), 201

#Route for get a To-Do Completed
@app.route('/todo/<int:id>/complete', methods=['GET'])
def complete_task(id):
    task = db.session.get(ToDo, id)

    if task is None:
        # If task is not found, return a 404 error
        return abort(404, description="Task not found")
    
    task.is_completed = True # Set a task as completed

    db.session.commit() # Save the changes to the database
    return jsonify({"message": "Task marked as complete"}), 200

#Route for get a To-Do Incompleted
@app.route('/todo/<int:id>/incomplete', methods=['GET'])
def incomplete_task(id):
    task = db.session.get(ToDo, id)

    if task is None:
        # If task is not found, return a 404 error
        return abort(404, description="Task not found")
    
    task.is_completed = False # Set a task as completed

    db.session.commit() # Save the changes to the database
    return jsonify({"message": "Task marked as incomplete"}), 200

# Route for edit a task by id
@app.route('/todo/<int:id>', methods=['PUT'])
def update_task(id):
    task = db.session.get(ToDo, id)
    data = request.json

    if task is None:
        # If task is not found, return a 404 error
        return abort(404, description="Task not found")

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)    
    task.is_completed = data.get('is_completed', task.is_completed)

    db.session.commit()
    return jsonify({"message": "Ok"}), 200

@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = db.session.get(ToDo, id)

    if task is None:
        # If task is not found, return a 404 error
        return abort(404, description="Task not found")

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Ok"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
