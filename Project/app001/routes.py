from flask import render_template, request, redirect, url_for, session
import re
from app001 import app
from app001.models import User
import pickle
import numpy as np
import csv

app.secret_key = "your secret key"


@app.route("/login/", methods=["GET", "POST"])
def login():
    # Output message if something goes wrong...
    msg = ""
    # Check if "username" and "password" POST requests exist (user submitted form)
    # username과 password에 입력값이 있을 경우
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # 쉬운 checking을 위해 변수에 값 넣기
        username = request.form["username"]
        password = request.form["password"]
        # MySQL DB에 해당 계정 정보가 있는지 확인
        account, check_password = User.login_check(username, password)
        if check_password:
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]
            session["role"] = account["role"]
            fromip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
            User.update_fromip(fromip, account["id"])
            # return 'Logged in successfully!'
            return redirect(url_for("home"))
        else:
            msg = "Incorrect username/password!"
    if "loggedin" in session:
        return redirect(url_for("home"))
    # Show the login form with message (if any)
    return render_template("login.html", msg=msg)


@app.route("/home")
def home():
    # Check if user is loggedin
    if "loggedin" in session:
        # User is loggedin show them the home page
        if session["role"] == "관리자":
            return render_template(
                "admin_home.html", username=session["username"], id=session["id"]
            )
        else:
            return render_template(
                "home.html", username=session["username"], session=session
            )
    # User is not loggedin redirect to login page
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    # Redirect to login page
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    # Check if user is loggedin
    if "loggedin" in session:
        account = User.get_information([session["id"]])
        if session["role"] == "관리자":
            return render_template("admin_profile.html", account=account)
        else:
            return render_template("profile.html", account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = "Creating User Page"
    # If already loggedin, redirect to home
    if "loggedin" in session:
        return redirect(url_for("home"))
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        username_already_exist = User.check_username_exist(username)
        email_already_exist = User.check_email_exist(email)
        if username_already_exist:
            msg = "That username is already exist"
        elif email_already_exist:
            msg = "That email is already exist"
        else:
            User.useradd(username, password, email)
            msg = "Create User Success!"
            return redirect(url_for("login"))
    return render_template("register.html", msg=msg)


@app.route("/survey", methods=["GET", "POST"])
def survey():
    msg = render_template("survey.html")
    return msg


@app.route("/survey_ans", methods=["GET", "POST"])
def survey_ans():
    model = pickle.load(open("./app001/model/model.t", "rb"))
    tool = pickle.load(open("./app001/model/tool.t", "rb"))

    age = request.form["age"]
    gender = request.form["gender"]
    a = request.form["a"]
    b = request.form["b"]
    c = request.form["c"]
    d = request.form["d"]
    e = request.form["e"]
    f = request.form["f"]
    g = request.form["g"]
    h = request.form["h"]
    i = request.form["i"]
    j = request.form["j"]
    k = request.form["k"]
    l = request.form["l"]
    m = request.form["m"]
    n = request.form["n"]

    print(gender, a, b, c, d, e, f, g, h, i, j, k, l, m, n)
    x = [[gender, a, b, c, d, e, f, g, h, i, j, k, l, m, n]]
    x = tool.transform(x).toarray()
    age_1 = [[age]]
    x = np.hstack([age_1, x])
    y_pre = model.predict(x)

    survey_content = (
        f"{age},{gender},{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m},{n}"
    )

    if y_pre[0] == "Positive":
        msg = "[당뇨병 초기 검진 결과] =====> 당신은 '당뇨병' 초기 증상이 의심됩니다! 빠른 시일내에 병원에서 검사해보시기바랍니다."
    else:
        msg = "[당뇨병 초기 검진 결과] =====> 당신은 '당뇨병' 초기 증상이 의심되지 않습니다! 오늘도 건강한 하루되시길 바랍니다!"
    return redirect(
        url_for("booking", msg=msg, survey_content=survey_content, pre=y_pre[0])
    )


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if "loggedin" in session:
        msg = request.args.get("msg")
        survey_content = request.args.get("survey_content")
        pre = request.args.get("pre")
        return render_template(
            "booking.html", msg=msg, survey_content=survey_content, pre=pre
        )

    return redirect(url_for("login"))


@app.route("/booking_ans", methods=["GET", "POST"])
def booking_ans():
    if "loggedin" in session:
        survey_content = request.form["survey_content"]
        hospital = request.form["hospital"]
        y = request.form["y"]
        m = request.form["m"]
        d = request.form["d"]
        User.update_survey(session["id"], survey_content, hospital, y, m, d)
        return render_template("survey_end.html")
    return render_template("login.html")


@app.route("/admin_booking", methods=["GET", "POST"])
def admin_booking():
    if "loggedin" in session:
        if session["role"] == "관리자":
            booking = User.get_bookinglist(session["id"])
            return render_template("admin_booking.html", booking=booking)
    return redirect(url_for("home"))


@app.route("/delete_booking", methods=["GET", "POST"])
def delete_booking():
    if "loggedin" in session:
        if session["role"] == "관리자":
            userid = request.args.get("userid")
            y = request.args.get("y")
            m = request.args.get("m")
            d = request.args.get("d")
            User.delete_booking(session["id"], userid, y, m, d)
            return redirect(url_for("admin_booking"))
    return redirect(url_for("home"))


@app.route("/check_booking", methods=["GET", "POST"])
def check_booking():
    if "loggedin" in session:
        if session["role"] == "관리자":
            userid = request.args.get("userid")
            y = request.args.get("y")
            m = request.args.get("m")
            d = request.args.get("d")
            survey_content = request.args.get("survey_content")
            check_booking = dict()
            check_booking["userid"] = userid
            check_booking["y"] = y
            check_booking["m"] = m
            check_booking["d"] = d
            check_booking["survey_content"] = survey_content.split(",")
            return render_template("check_booking.html", check_booking=check_booking)
    return redirect(url_for("home"))


@app.route("/save_survey", methods=["GET", "POST"])
def save_survey():
    if "loggedin" in session:
        if session["role"] == "관리자":
            survey_content = request.form["survey_content"]
            diaclass = request.form["Dia"]
            userid = request.form["userid"]
            y = request.form["y"]
            m = request.form["m"]
            d = request.form["d"]
            print(f"{userid},{y},{m},{d} ")
            survey_content = survey_content.replace("'","")
            survey_content = survey_content.replace("[","")
            survey_content = survey_content.replace("]","")
            survey_content = f"'{survey_content},{diaclass}'"
            print(survey_content)
            User.save_survey(survey_content)
            User.delete_booking(session["id"], userid,y, m, d)
            return redirect(url_for("admin_booking"))
    return redirect(url_for("home"))


@app.route("/print_csv",methods=["GET","POST"])
def print_csv():
    if "loggedin" in session:
        if session["role"] == "관리자":
            get_list = User.get_save_survey()
            f = open('./app001/dataset/save_survey.csv','a',newline="")
            wr = csv.writer(f)
            wr.writerows(get_list)    
            f.close()
    return "저장완료!"
