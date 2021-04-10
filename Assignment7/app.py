from flask import Flask, request, redirect, render_template, session, url_for, jsonify
import secrets
from getpass import getpass
from mysql.connector import connect
import json

app=Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key=secrets.token_bytes(16)

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
    if "username" in session:
        return render_template("member.htm", name=session["username"])
    else:
        return redirect("/")

@app.route("/success")
def forSuccess():
    if "signup" in session:
        return render_template("success.htm")
    else:
        return redirect("/")

@app.route("/signup", methods=["POST"])
def signUp():
    name=request.form["name"]
    account=request.form["account"]
    password=request.form["password"]
    if name and account and password:
        with userdb.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = %s", (account,))
            sqlresult=cursor.fetchone()
        if sqlresult:
            return redirect(url_for("forError", message="帳號已經被註冊"))
        else:
            with userdb.cursor() as cursor:
                cursor.execute("INSERT INTO user (name, username, password) VALUES (%s, %s, %s)", (name, account, password))
                userdb.commit()
            session["signup"]=True
            return redirect("/success")
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
        session["username"]=sqlresult[1]
        return redirect("/member")
    else:
        return redirect(url_for("forError", message="帳號或密碼輸入錯誤"))

@app.route("/signout")
def signOut():
    session.pop("username", None)
    return redirect("/")

@app.route("/backhome")
def backHome():
    session.pop("signup", None)
    return redirect("/")

@app.route("/api/users")
def getData():
    if "username" in session:
        account=request.args.get("username")
        with userdb.cursor() as cursor:
            cursor.execute("SELECT id, name, username FROM user WHERE username = %s", (account, ))
            sqlresult=cursor.fetchone()
        if sqlresult:
            return jsonify({"data":{"id":sqlresult[0], "name":sqlresult[1], "username":sqlresult[2]}})
        else:
            return jsonify({"data":"null"})
    else:
        return redirect(url_for("forError", message="需登入取得權限"))

@app.route("/api/user", methods=["POST"])
def updateData():
    newname=request.json
    try:
        with userdb.cursor() as cursor:
            cursor.execute("UPDATE user SET name = %s WHERE name = %s", (newname["name"], session["username"]))
            userdb.commit()
        session["username"] = newname["name"]
        return jsonify({"ok":True})
    except:
        return jsonify({"error":True})


app.run(port=3000)