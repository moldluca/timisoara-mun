from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message


app = Flask(__name__)

app.secret_key = 'supersecretkey'

app.config['MAIL_SERVER'] = 'mail.timisoara-mun.ro'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True  # Port 465 uses SSL
app.config['MAIL_USE_TLS'] = False  # Do NOT set TLS when using SSL
app.config['MAIL_USERNAME'] = 'delegate.registration@timisoara-mun.ro'
app.config['MAIL_PASSWORD'] = 'InregistrareMUN1'  # pune parola reală aici
app.config['MAIL_DEFAULT_SENDER'] = ('MUN Timisoara', 'delegate.registration@timisoara-mun.ro')

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():
    # Capture form data
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    date_of_birth = request.form.get('dateOfBirth')
    nationality = request.form.get('nationality')
    address = request.form.get('address')
    motivation = request.form.get('motivation')
    hear_about = request.form.get('hearAbout')

    # Debug: print captured form data
    print(f"Received data: {first_name} {last_name}, {email}, {phone}, {date_of_birth}, {nationality}, {address}, {motivation}, {hear_about}")

    # Compose the email
    subject = "Delegate Registration - MUN Timișoara"
    body = f"""
    Hi {first_name} {last_name},

    Thank you for registering for MUN Timișoara 2025. Below are your submitted details:

    Name: {first_name} {last_name}
    Email: {email}
    Phone: {phone}
    Date of Birth: {date_of_birth}
    Nationality: {nationality}
    Address: {address}
    How did you hear about MUN Timișoara: {hear_about}
    Motivation: {motivation}

    We will get back to you soon. If you have any questions, feel free to contact us.

    Best regards,
    MUN Timișoara Team
    """

    # Send the email to the user
    msg = Message(
        subject=subject,
        recipients=[email],  # Send email to the address entered in the form
        body=body,
    )

    try:
        # Send the email
        mail.send(msg)
        flash('Registration successful! A confirmation email has been sent to your email address.', 'success')
        return redirect(url_for('delegates'))  # Redirect back to the registration page (or a success page)
    except Exception as e:
        print(f"Error: {e}")
        flash('There was an error with your registration. Please try again later.', 'error')
        return redirect(url_for('delegates'))




@app.route("/committees/<comitet>")
def comitete(comitet):
    return render_template("comitete.html", comitet=comitet)



@app.route("/delegates-registration")
def delegates():
    return render_template("formular-delegati.html")









@app.route('/loginstaffmuntm')
def loginstaff():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)