import sys
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Homepage
@app.route("/", methods=["POST", "GET"])
def home():
    username = None
    if request.method == "POST":
        username = request.form["username"]
        print('Hello world!', file=sys.stderr)
        return redirect(url_for("chatroom", username=username))
    return render_template("index.html", username=username)

# Chatroom
@app.route("/chatroom/<username>")
def chatroom(username):
    return render_template("chatroom.html", username=username)

if __name__ == "__main__":
    app.run()
