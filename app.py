from flask import Flask, render_template, request, flash, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapp123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "MyPythonProtfolio@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        # Render email template with form data
        email_body = render_template("email.html", first_name=first_name, last_name=last_name, date=date)

        # Send email message
        message = Message(subject="Form Application",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          html=email_body)
        mail.send(message)

        flash(f"Thank you {first_name}, Your form was submitted successfully!", "success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)