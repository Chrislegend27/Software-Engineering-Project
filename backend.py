from flask import Flask, render_template, request, redirect, url_for
import sys

app = Flask(__name__)

# Homepage
@app.route("/", methods=["POST", "GET"])
def home():
    username = None
    if request.method == "POST":
        username = request.form["nm"]
        return redirect(url_for("chatroom", usr=username))
    return render_template("index.html", usr=username)

# Chatroom
@app.route("/chatroom/<usr>", methods=["GET", "POST"])
def chatroom(usr):
    if request.method == "POST":
        # Handle form submission here
        pass
    return render_template("chatroom.html", usr=usr)

if __name__ == "__main__":
    app.run()
