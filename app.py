from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])   # GET is when the user is accessing the website through the url and POST is when they submit the form
def index():
    print(request.method)
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        occupation = request.form["occupation"]

    return render_template("index.html")


app.run(debug=True, port=5001)