from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.message



# Homepage
@app.route("/", methods=["POST", "GET"])
def home():
    
    username = None
    if request.method == "POST":
        # Check if the signup button was clicked
        if 'signup' in request.form:
            return redirect(url_for("signup"))
        username = request.form["nm"]
        return redirect(url_for("chatroom", usr=username))
    return render_template("index.html", usr=username)

# Chatroom
@app.route("/chatroom/<usr>", methods=["GET"])
def chatroom(usr):
    #retrieve database message:
    messages = Message.query.all()
    #render template
    return render_template("chatroom.html", usr=usr, messages=messages)

# SignUp Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Handle normal login submission
    if 'nm' in request.form:
        username = request.form["nm"]
        return redirect(url_for("chatroom", usr=username))
    return render_template("signupPage.html")

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    #Save to database code
    new_message = Message(username=username, message=message)
    db.session.add(new_message)
    db.session.commit()
    # Emit the message to all clients, including the sender's username
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)


if __name__ == "__main__":
        # Create an application context for the database operation
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
