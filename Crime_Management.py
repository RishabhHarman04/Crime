from flask import Flask, session
from flask import render_template
from flask import request
import sqlite3

app = Flask('__name__')
app.secret_key = "Ayush"


@app.route('/')
def homepage():
    return render_template("Content.html")


@app.route('/CAlogin')
def Admin():
    return render_template("Login.html")


@app.route('/Alogin', methods=["Post"])
def admin():
    name = request.form["aid"]
    password = request.form["pass"]

    if name == "admin" and password == '12345':
        return render_template("AdminOp.html")
    else:
        return "login failed"


@app.route('/CUlogin')
def User():
    return render_template("UserContent.html")


@app.route('/Uregister', methods=["GET"])
def regform():
    return render_template("Register.html")


@app.route('/AddUserdetails', methods=["Post"])
def adddetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["uname"]
            address = request.form["addr"]
            email = request.form["email"]
            phone = request.form["phone"]
            password = request.form["pass"]

            t = (name, address, email, phone, password)
            with sqlite3.connect("Crime_Management.db") as con:
                cur = con.cursor()
                sql = """INSERT INTO Ulogin_table3(name,address,email,phone,password)VALUES(?,?,?,?,?);"""
                cur.execute(sql, t)
                con.commit()
                msg = "User details successfully registered"

        except:
            con.rollback()
            msg = "Cannot add the user details please try again later"
        finally:
            con.close()
            return render_template("Success.html", msg=msg)


@app.route("/view")
def view():
    con = sqlite3.connect("Crime_Management.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("Select * from Ulogin_table3")
    rows = cur.fetchall()
    return render_template("View.html", rows=rows)


@app.route('/Ulogin', methods=['GET'])
def userlog():
    return render_template("UserLogin.html")


@app.route('/verify', methods=["Get", "Post"])
def verifyuser():
    if request.method == "POST":
        uid = request.form["uid"]
        x = uid
        password = request.form["pass"]
        con = sqlite3.connect("Crime_Management.db")
        cur = con.cursor()
        sql = "select * from Ulogin_table3 where email=?"
        cur.execute(sql, (x,))
        result = cur.fetchall()
        if result[0][2] == uid and result[0][4] == password:
            session['email'] = request.form['uid']
            return render_template('Complaint.html')
        else:
            return "Can't Login"
    else:
        return "This will not work"


@app.route('/profile', methods=['Post'])
def profile():
    if 'email' in session:
        email = session['email']
        con = sqlite3.connect("Crime_Management.db")
        cur = con.cursor()
        sql = "select name from Ulogin_table3 where email=?"
        cur.execute(sql, (email,))
        r = cur.fetchall()
        a = r[0][0]
        description = request.form["dis"]
        remark = request.form["rem"]
        date = request.form["date"]
        t = (description, remark, date, a)
        with sqlite3.connect("Crime_Management.db") as con:
            cur = con.cursor()
            sql = """INSERT INTO crime_report1(description, remark,Report_Date, name)VALUES(?,?,?,?);"""
            cur.execute(sql, t)
            con.commit()
            return render_template("Success2.html")

    else:
        description = request.form["dis"]
        remark = request.form["rem"]
        date = request.form["date"]
        y = (description, remark, date)
        with sqlite3.connect("Crime_Management.db") as con:
            cur = con.cursor()
            q = """INSERT INTO crime_report1(description, remark,Report_Date)VALUES(?,?,?);"""
            cur.execute(q, y)
            con.commit()
            return "Your report is successfully stored anonymously"


@app.route('/EditProfile', methods=["GET"])
def ed1():
    return render_template("update.html")


@app.route('/Cupdate', methods=["POST"])
def updating():
    mno = request.form["mon"]
    k = mno

    con = sqlite3.connect("Crime_Management.db")
    cur = con.cursor()
    q = "select * from Ulogin_table3 where phone=?"
    cur.execute(q, (k,))

    result = cur.fetchall()
    print(result)
    if (result[0][1]) != None:
        return render_template("updateEntry.html")


@app.route('/update', methods=["POST"])
def up_1():
    name1 = request.form["user_name"]
    addr1 = request.form["addrs"]
    mob1 = request.form["cmon"]

    prev_no = request.form["mon1"]
    email12 = request.form["email1"]
    t = (name1, mob1, addr1, email12, prev_no)
    e = sqlite3.connect("Crime_Management.db")
    with e as con:
        try:
            cur = con.cursor()
            cur.execute("update Ulogin_table2 set name=?,address=?,phone=?,email=?  where phone=?", t)
            con.commit()
            return "Record updated successfully!"
        except:
            con.rollback()


@app.route('/Cguest')
def guest():
    return render_template("Guest.html")


@app.route('/Viewallcrime')
def view1():
    con = sqlite3.connect("Crime_Management.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select description,remark,Report_Date,name from crime_report1")
    rows = cur.fetchall()
    return render_template("view1.html", rows=rows)


@app.route('/SearchCrime', methods=["GET"])
def serching():
    return render_template("Csearch.html")


@app.route('/search1', methods=["POST"])
def search12():
    d1 = request.form["date1"]
    con = sqlite3.connect("Crime_Management.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select description,remark,Report_Date,name from crime_report1 where Report_Date=? ", (d1,))
    rows = cur.fetchall()
    return render_template("view1.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
