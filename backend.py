from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Message {self.username}: {self.message}>'

# Homepage
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form)
        action = request.form.get('action')
        print(f"Action recieved: {action}")
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for("chatroom", usr=username))
        else:
            flash("Invalid username or password")
            # Redirect to the same home URL to ensure fresh load
            return redirect(url_for("home"))

    return render_template("index.html")

# Chatroom
@app.route("/chatroom/<usr>", methods=["GET"])
def chatroom(usr):
    if 'username' not in session or session['username'] != usr:
        return redirect(url_for("home"))
    messages = Message.query.all()
    return render_template("chatroom.html", usr=usr, messages=messages)

# SignUp Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already taken. Choose a different username.")
            return redirect(url_for("signup"))

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for("home"))
        
    return render_template("signupPage.html")

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    new_message = Message(username=username, message=message)
    db.session.add(new_message)
    db.session.commit()
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
