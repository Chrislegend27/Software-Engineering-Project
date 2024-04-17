from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.secret_key = "YOUR_VERY_SECRET_KEY"  # Change this to a more secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)
socketio = SocketIO(app)
messages = []  # This will store our messages and their timestamps

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route("/", methods=["POST", "GET"])
def home():
    if 'user' in session:
        return redirect(url_for("chatroom", usr=session['user']))

    if request.method == "POST":
        session.permanent = True
        username = request.form["nm"]
        password = request.form["password"]
        found_user = User.query.filter_by(name=username).first()

        if found_user and found_user.check_password(password):
            session['user'] = username
            flash("Logged in successfully!")
            return redirect(url_for("chatroom", usr=username))
        elif found_user:
            flash("Wrong password!")
        else:
            new_user = User(name=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            flash("User created and logged in!")
            return redirect(url_for("chatroom", usr=username))

    return render_template("index.html")

@app.route("/chatroom/<usr>", methods=["GET"])
def chatroom(usr):
    current_time = datetime.now()
    valid_messages = [msg for msg in messages if (current_time - msg['timestamp']) < timedelta(minutes=2)]
    return render_template("chatroom.html", usr=usr, messages=valid_messages)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    messages.append({'username': username, 'message': message, 'timestamp': datetime.now()})
    emit('receive_message', data, broadcast=True)

def cleanup_messages():
    while True:
        time.sleep(60)
        with app.app_context():
            global messages
            current_time = datetime.now()
            messages = [msg for msg in messages if (current_time - msg['timestamp']) < timedelta(minutes=2)]
g
if __name__ == "__main__":
    from threading import Thread
    cleanup_thread = Thread(target=cleanup_messages)
    cleanup_thread.start()
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)  # Set debug as False for production-like environment
