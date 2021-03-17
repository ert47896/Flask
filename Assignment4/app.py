from flask import Flask, request, redirect, render_template, session
import secrets

app=Flask(__name__)
app.secret_key=secrets.token_bytes(16)

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/member")
def forMember():
    if "username" in session:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route("/error")
def forError():
    return render_template("error.html")

@app.route("/signin", methods=["POST"])
def signIn():
    account=request.form["account"]
    password=request.form["password"]
    if account=="test" and password=="test":
        session["username"]=account
        return redirect("/member")
    else:
        return redirect("/error")

@app.route("/signout")
def signOut():
    session.pop("username", None)
    return redirect("/")

app.run(port=3000)