from flask import Flask, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
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
    tasks = ToDo.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

#Route for get a specific To-Do by id
@app.route('/todo/<int:id>', methods=['GET'])
def get_task(id):
    task = ToDo.query.get(id)
    if task is None:
        abort(404)  # Si el To-Do no se encuentra, devuelve un error 404
    return jsonify(task.to_dict()), 200  # Devuelve el To-Do en formato JSON

# Ruta para crear un nuevo To-Do
@app.route('/todo', methods=['POST'])
def create_task():
    data = request.json
    new_task = ToDo(
        title=data.get('title'),
        description=data.get('description'),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

#Route for get a To-Do Completed
@app.route('/todo/<int:id>/complete', methods=['POST'])
def complete_task(id):
    task = ToDo.query.get(id)
    if task is None:
        # If task is not found, return a 404 error
        return abort(404, description="Task not found")
    
    task.is_completed = True # Set a task as completed
    db.session.commit() # Save the changes to the database
    return redirect(url_for('get_tasks')) # Redirect to the task list

# Ruta para editar un To-Do existente por ID
@app.route('/todo/<int:id>', methods=['PUT'])
def update_task(id):
    task = ToDo.query.get(id)
    data = request.json

    if not task:
        return jsonify({"error": "To-Do not found"}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)    
    task.date_created = data.get('date_created', task.date_created),
    task.is_completed = data.get('is_completed', task.is_completed)

    db.session.commit()
    return jsonify(task.to_dict())


# Ruta para editar un To-Do existente por ID
# @app.route('/todo/<int:id>', methods=['PATCH'])
# def update_detail_todo(id):
#     todo = ToDo.query.get(id)
#     data = request.json

#     if not todo:
#         return jsonify({"error": "To-Do not found"}), 404

#     todo.title = data.get('title', todo.title)
#     todo.description = data.get('description', todo.description)    
#     todo.is_completed = data.get('is_completed', todo.is_completed)

#     db.session.commit()
#     return jsonify(todo.to_dict())

# Ruta para eliminar un To-Do existente
@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_task(id):
    todo = ToDo.query.get(id)

    if not todo:
        return jsonify({"error": "To-Do not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "To-Do deleted"}), 200

@app.route('/todo', methods=['GET'])
def get_tasks():
    tasks = ToDo.query.all()
    return {
        "tasks": [
            {"id": task.id, "title": task.title, "is_completed": task.is_completed}
            for task in tasks
        ]
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
