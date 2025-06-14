from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS so our React client at http://localhost:3000 can access
CORS(app)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/messages', methods=['GET'])
def get_messages():
    """
    Return all messages in ascending order of creation time.
    """
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    """
    Create a new message with JSON payload { body, username }.
    """
    data = request.get_json()
    message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """
    Update the body of an existing message.
    """
    data = request.get_json()
    message = Message.query.get_or_404(id)
    message.body = data.get('body', message.body)
    message.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """
    Delete a message by ID.
    """
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)