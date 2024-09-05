from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    #date_created = db.Column(db.DateTime, default=datetime.now)
    is_completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            #'date_created': self.date_created.isoformat(),
            'is_completed': self.is_completed
        }

# Ruta para obtener todos los To-Dos
@app.route('/todos', methods=['GET'])
def get_all_todos():
    todos = ToDo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200

#Route for get a specific To-Do by id
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = ToDo.query.get(id)
    if todo is None:
        abort(404)  # Si el To-Do no se encuentra, devuelve un error 404
    return jsonify(todo.to_dict()), 200  # Devuelve el To-Do en formato JSON

# Ruta para crear un nuevo To-Do
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = ToDo(
        title=data.get('title'),
        description=data.get('description'),
        is_completed=data.get('is_completed', False)
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# Ruta para editar un To-Do existente por ID
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = ToDo.query.get(id)
    data = request.json

    if not todo:
        return jsonify({"error": "To-Do not found"}), 404

    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)    
    todo.date_created = data.get('date_created', todo.date_created),
    todo.is_completed = data.get('is_completed', todo.is_completed)

    db.session.commit()
    return jsonify(todo.to_dict())


# Ruta para editar un To-Do existente por ID
# @app.route('/todos/<int:id>', methods=['PATCH'])
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
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = ToDo.query.get(id)

    if not todo:
        return jsonify({"error": "To-Do not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "To-Do deleted"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
