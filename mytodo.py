from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'{self.id} {self.content}'


# db.create_all()
def todo_serializer(todo):
    return {
        'id': todo.id,
        'content': todo.content
    }


@app.route('/content', methods=['GET'])
def index():
    todo = Todo.query.all()
    return jsonify([*map(todo_serializer, todo)])


@app.route('/content', methods=['DELETE'])
def delete_task():
    todo_id = request.args.get('id')
    if not todo_id:
        return jsonify({'message': 'Todo id is required'}), 400
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200


@app.route('/content', methods=['POST', 'PUT'])
def indexOther():
    if request.method == 'POST':
        content = request.json.get('content')
        if not content:
            return jsonify({'message': 'content is required'}), 400
        todo = Todo(content=content)
        db.session.add(todo)
        db.session.commit()
        return jsonify({'message': 'Todo created successfully'}), 201
    elif request.method == 'PUT':
        todo_id = request.args.get('id')
        if not todo_id:
            return jsonify({'message': 'Todo id is required'}), 400
        todo = Todo.query.filter_by(id=todo_id).first()
        if not todo:
            return jsonify({'message': 'Todo not found'}), 404
        content = request.json.get('content')
        if not content:
            return jsonify({'message': 'content is required'}), 400
        todo.content = content
        db.session.commit()
        return jsonify({'message': 'Todo updated successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
