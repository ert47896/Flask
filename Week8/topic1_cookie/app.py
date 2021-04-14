from flask import Flask, request, redirect, render_template, make_response
import secrets
import time

app=Flask(__name__)
cookieStatus={}

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/member")
def forMember():
    account=request.cookies.get("sessionid")
    if account in cookieStatus and time.time() < cookieStatus[account]["expires_time"]:
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
        secretKey=secrets.token_hex(16)
        expiresTime=time.time()+20*60
        cookieStatus[secretKey]={}
        cookieStatus[secretKey]["account"]=account
        cookieStatus[secretKey]["expires_time"]=expiresTime
        resp=make_response(redirect("/member"))
        resp.set_cookie(key="sessionid", value=secretKey, expires=expiresTime, httponly=True, samesite="Strict")
        return resp
    else:
        return redirect("/error")

@app.route("/signout")
def signOut():
    account=request.cookies.get("sessionid")
    cookieStatus.pop(account)
    outResp=make_response(redirect("/"))
    outResp.set_cookie(key="sessionid", value="", expires=0)
    return outResp

app.run(port=3000)