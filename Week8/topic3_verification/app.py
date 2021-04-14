from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response
import time
from getpass import getpass
from mysql.connector import connect
import re
import secrets

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
    sessionid=request.cookies.get("sessionid")
    with userdb.cursor() as cursor:
        cursor.execute("SELECT name, sessionid_create_time FROM user WHERE sessionid = %s", (sessionid,))
        sqlresult=cursor.fetchone()
    if sqlresult and time.time() < float(sqlresult[1]):
        return render_template("member.htm", name=sqlresult[0])
    else:
        return redirect("/")

@app.route("/success")
def forSuccess():
    return render_template("success.htm")

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
                    cursor.execute("SELECT username FROM user WHERE username = %s", (account,))
                    sqlresult=cursor.fetchone()
                if sqlresult:
                    return redirect(url_for("forError", message="帳號已經被註冊"))
                else:
                    with userdb.cursor() as cursor:
                        cursor.execute("INSERT INTO user (name, username, password) VALUES (%s, %s, %s)", (name, account, password))
                        userdb.commit()
                    return redirect("/success")
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
        cursor.execute("SELECT username FROM user WHERE username = %s AND password = %s", (account, password))
        sqlresult=cursor.fetchone()
    if sqlresult:
        key=secrets.token_hex(16)
        expiresTime=time.time()+10*60
        with userdb.cursor() as cursor:
            cursor.execute("UPDATE user SET sessionid = %s, sessionid_create_time = %s WHERE username = %s", (key, expiresTime, sqlresult[0]))
            userdb.commit()
        respAccount=make_response(redirect("/member"))
        respAccount.set_cookie(key="sessionid", value=key, expires=expiresTime, httponly=True, samesite="Strict")
        return respAccount
    else:
        return redirect(url_for("forError", message="帳號或密碼輸入錯誤"))

@app.route("/signout")
def signOut():
    sessionid=request.cookies.get("sessionid")
    with userdb.cursor() as cursor:
        cursor.execute("UPDATE user SET sessionid = %s, sessionid_create_time = %s WHERE sessionid = %s", (None, None, sessionid))
        userdb.commit()
    signOutResp=make_response(redirect("/"))
    signOutResp.set_cookie(key="sessionid", value="", expires=0)
    return signOutResp

@app.route("/backhome")
def backHome():
    return redirect("/")

@app.route("/api/users")
def getData():
    sessionid=request.cookies.get("sessionid")
    with userdb.cursor() as cursor:
        cursor.execute("SELECT sessionid, sessionid_create_time FROM user WHERE sessionid = %s", (sessionid,))
        sqlresult=cursor.fetchone()
    if sqlresult and time.time() < float(sqlresult[1]):
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
        sessionid=request.cookies.get("sessionid")
        with userdb.cursor() as cursor:
            cursor.execute("SELECT name FROM user WHERE sessionid = %s", (sessionid,))
            sqlresult=cursor.fetchone()
        try:
            with userdb.cursor() as cursor:
                cursor.execute("UPDATE user SET name = %s WHERE name = %s", (newname["name"], sqlresult[0]))
                userdb.commit()
            return jsonify({"ok":True})
        except:
            return jsonify({"error":True})
    else:
        return jsonify({"null":"Need data input!"})

app.run(port=3000)