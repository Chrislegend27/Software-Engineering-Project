from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Homepage
@app.route("/", methods=["POST", "GET"])
def home():
    username = None
    if request.method == "POST":
        username = request.form["nm"]
        return redirect(url_for("chatroom", usr=username))
    return render_template("index.html", usr=username)

# Chatroom
@app.route("/chatroom/<usr>", methods=["GET"])
def chatroom(usr):
    return render_template("chatroom.html", usr=usr)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    # Emit the message to all clients, including the sender's username
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True)
