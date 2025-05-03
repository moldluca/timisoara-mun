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
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Compose the email to the user
    msg = Message(
        subject="We received your message!",
        recipients=[email],  # send TO the email from the form
        body=f"Hi {name},\n\nThank you for reaching out to MUN Timișoara!\n\nYou wrote:\n{message}\n\nWe will get back to you as soon as possible.\n\nBest regards,\nMUN Timișoara Team"
    )

    try:
        mail.send(msg)
        return "Confirmation email sent successfully!"
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while sending the email."



# @app.route("/comitete")
# def comitete():
    # return render_template("comitete.html")



@app.route("/delegates-registration")
def delegates():
    return render_template("formular-delegati.html")









@app.route('/loginstaffmuntm')
def loginstaff():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)