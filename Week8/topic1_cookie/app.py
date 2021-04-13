from flask import Flask, request, redirect, render_template, make_response
import secrets
import time

app=Flask(__name__)
app.secret_key=secrets.token_bytes(16)

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/member")
def forMember():
    account=request.cookies.get("username")
    if account:
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
        resp=make_response(redirect("/member"))
        resp.set_cookie(key="username", value=account, expires=time.time()+10*60, httponly=True, samesite="Strict")
        return resp
    else:
        return redirect("/error")

@app.route("/signout")
def signOut():
    outResp=make_response(redirect("/"))
    outResp.set_cookie(key="username", value="", expires=0)
    return outResp

app.run(port=3000)