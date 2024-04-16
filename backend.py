from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Homepage
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # Check if the signup button was clicked
        if 'signup' in request.form:
            return redirect(url_for("signup"))
        
        # Handle normal login submission
        if 'nm' in request.form:
            username = request.form["nm"]
            return redirect(url_for("chatroom", usr=username))

    return render_template("index.html")

# Chatroom
@app.route("/chatroom/<usr>", methods=["GET", "POST"])
def chatroom(usr):
    # Your chatroom logic
    return render_template("chatroom.html", usr=usr)

# SignUp Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Handle normal login submission
    if 'nm' in request.form:
        username = request.form["nm"]
        return redirect(url_for("chatroom", usr=username))
    return render_template("signupPage.html")

if __name__ == "__main__":
    app.run()
