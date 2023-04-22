from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

# Set the secret key for the app
app.config["SECRET_KEY"] = "myapp123"

# Set the URI for the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Set the configuration for the email server
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "MyPythonProtfolio@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

# Create a SQLAlchemy object and bind it to the app
db = SQLAlchemy(app)

# Create a Mail object and bind it to the app
mail = Mail(app)

# Define a database model for the form data
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

# Define a route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # Create a new form object with the extracted data
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)

        # Add the form object to the database and commit the changes
        db.session.add(form)
        db.session.commit()

        # Render the email template with the form data
        email_body = render_template("email.html", first_name=first_name, last_name=last_name, date=date)

        # Create a new email message with the rendered email template and send it
        message = Message(subject="Form Application",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          html=email_body)
        mail.send(message)

        # Flash a success message to the user
        flash(f"Thank you {first_name}, Your form was submitted successfully!", "success")

    # Render the index template
    return render_template("index.html")

# Start the app
if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
        db.create_all()
        # Run the app in debug mode on port 5001
        app.run(debug=True, port=5001)
