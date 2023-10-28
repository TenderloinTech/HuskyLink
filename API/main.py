from flask import Flask, request, Response
import psycopg2
import json

# Create a Flask app
app = Flask(__name__)



# Define a route
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/api/v1/login", methods=["POST"])
def login():
    user = request.form.get('username')
    password = request.form.get('password')

    conn = psycopg2.connect(json.loads(open("API/config.json").read())["cockroach"])

    with conn.cursor() as cur:
        cur.execute(f"select * from testlogin where username='{user}'")
        res = cur.fetchall()
        conn.commit()
        if len(res) != 1:
            return Response(json.dumps({"result": {"password": False}}), content_type="application/json")
        if res[0][1] == password:
            return Response(json.dumps({"result": {"password": True}}), content_type="application/json")
    return Response(json.dumps({"result": {"password": False}}), content_type="application/json")

@app.route("/api/v1/createAccount", methods=["POST"])
def create():

    # Parameters Required
    user = request.form.get('username')
    password = request.form.get('password')
    

    conn = psycopg2.connect(json.loads(open("API/config.json").read())["cockroach"])

    with conn.cursor() as cur:
        cur.execute(f"insert into users where username='{user}'")
        res = cur.fetchall()
        conn.commit()
        if len(res) != 0:
            if res[0][0] == user:
                return Response(json.dumps({"result": {"success": False, "message": "Username exists"}})), 400

    conn = psycopg2.connect(json.loads(open("API/config.json").read())["cockroach"])

    with conn.cursor() as cur:
        cur.execute(f"insert into testLogin (username, pass) values ('{user}', '{password}')")
        conn.commit()
    return Response(json.dumps({"result": {"success": True, "message": "ok"}}), content_type="application/json")

@app.route("/api/v1/listAllUsers", methods=["GET"])
def lists():
    conn = psycopg2.connect(json.loads(open("API/config.json").read())["cockroach"])

    with conn.cursor() as cur:
        cur.execute(f"select username from testlogin")
        res = cur.fetchall()
        conn.commit()
        return Response(json.dumps(res), content_type="application/json")

@app.route("/api/v1/sortByTag/<tag>")
def sortTag(tag):
    conn = psycopg2.connect(json.loads(open("API/config.json").read())["cockroach"])

    with conn.cursor() as cur:
        cur.execute(f"select username from testlogin")
        res = cur.fetchall()
        conn.commit()
        return Response(json.dumps(res), content_type="application/json")

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')