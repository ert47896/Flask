from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response
import time
from getpass import getpass
from mysql.connector import connect
import json
import re

app=Flask(__name__, static_folder="public", static_url_path="/")

userdb=connect(
    host="localhost",
    user=input("Enter username: "),
    password=getpass("Enter password: "),
    database="assignment6"
)

@app.route("/")
def index():
    return render_template("homepage.htm")

@app.route("/error")
def forError():
    error_message=request.args.get("message")
    if error_message:
        return render_template("error.htm", errorMessage=error_message)
    else:
        return redirect("/")

@app.route("/member")
def forMember():
    accountStatus=request.cookies.get("username")
    if accountStatus:
        return render_template("member.htm", name=accountStatus)
    else:
        return redirect("/")

@app.route("/success")
def forSuccess():
    signupStatus=request.cookies.get("signup")
    if signupStatus:
        return render_template("success.htm")
    else:
        return redirect("/")

@app.route("/signup", methods=["POST"])
def signUp():
    name=request.form["name"]
    account=request.form["account"]
    password=request.form["password"]
    lenAccount=len(account)
    lenPassword=len(password)
    pattern = r"^[a-zA-Z0-9]+$"
    if name and account and password:
        if lenAccount >= 4 and lenAccount <= 16 and re.fullmatch(pattern, account):
            if lenPassword >= 4 and lenPassword <= 16 and re.fullmatch(pattern, password):
                with userdb.cursor() as cursor:
                    cursor.execute("SELECT * FROM user WHERE username = %s", (account,))
                    sqlresult=cursor.fetchone()
                if sqlresult:
                    return redirect(url_for("forError", message="帳號已經被註冊"))
                else:
                    with userdb.cursor() as cursor:
                        cursor.execute("INSERT INTO user (name, username, password) VALUES (%s, %s, %s)", (name, account, password))
                        userdb.commit()
                    respSignup=make_response(redirect("/success"))
                    respSignup.set_cookie(key="signup", value="Ture", expires=time.time()+10*60, httponly=True, samesite="Strict")
                    return respSignup
            else:
                return redirect(url_for("forError", message="密碼請輸入4~16位英數字"))
        else:
            return redirect(url_for("forError", message="帳號請輸入4~16位英數字"))
    else:
        return redirect(url_for("forError", message="請輸入資料"))

@app.route("/signin", methods=["POST"])
def signIn():
    account=request.form["account"]
    password=request.form["password"]
    with userdb.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (account, password))
        sqlresult=cursor.fetchone()
    if sqlresult:
        respAccount=make_response(redirect("/member"))
        respAccount.set_cookie(key="username", value=sqlresult[1], expires=time.time()+10*60, httponly=True, samesite="Strict")
        return respAccount
    else:
        return redirect(url_for("forError", message="帳號或密碼輸入錯誤"))

@app.route("/signout")
def signOut():
    signOutResp=make_response(redirect("/"))
    signOutResp.set_cookie(key="username", value="", expires=0)
    return signOutResp

@app.route("/backhome")
def backHome():
    backHomeResp=make_response(redirect("/"))
    backHomeResp.set_cookie(key="signup", value="", expires=0)
    return backHomeResp

@app.route("/api/users")
def getData():
    accountStatus=request.cookies.get("username")
    if accountStatus:
        account=request.args.get("username")
        if account:
            with userdb.cursor() as cursor:
                cursor.execute("SELECT id, name, username FROM user WHERE username = %s", (account, ))
                sqlresult=cursor.fetchone()
            if sqlresult:
                return jsonify({"data":{"id":sqlresult[0], "name":sqlresult[1], "username":sqlresult[2]}})
            else:
                return jsonify({"data":"null"})
        else:
            return jsonify({"data":"Need data input!"})
    else:
        return redirect(url_for("forError", message="需登入取得權限"))

@app.route("/api/user", methods=["POST"])
def updateData():
    newname=request.json
    if newname["name"]:
        accountStatus=request.cookies.get("username")
        try:
            with userdb.cursor() as cursor:
                cursor.execute("UPDATE user SET name = %s WHERE name = %s", (newname["name"], accountStatus))
                userdb.commit()
            newresp=make_response(jsonify({"ok":True}))
            newresp.set_cookie(key="username", value=newname["name"], expires=time.time()+10*60, httponly=True, samesite="Strict")
            return newresp
        except:
            return jsonify({"error":True})
    else:
        return jsonify({"null":"Need data input!"})

app.run(port=3000)