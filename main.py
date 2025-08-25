from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from models import db, Registration
from functools import wraps
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

users = {
    "dragos@timisoara-mun.ro": "dragosSecretariatMunIntern",
    "cristiana@timisoara-mun.ro": "cristianaSecretariatMunIntern",
    "erol@timisoara-mun.ro": "erolSecretariatMunIntern",
    "secretariat@timisoara-mun.ro": "secretariatSecretariatMunIntern",
    "luca.vasiu@timisoara-mun.ro": "lucaSecretariatMunIntern",
    "delegate.registration@timisoara-mun.ro": "delegateSecretariatMunIntern"
}


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') == 'True'
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (
    os.environ.get('MAIL_DEFAULT_SENDER_NAME'),
    os.environ.get('MAIL_DEFAULT_SENDER_EMAIL')
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app) 


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('loginstaff'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

# ---------------------------------------- MAIL INSCRIERI ----------------------------------------

import requests
import os

@app.route('/send_mail', methods=['POST'])
def send_mail():
    print(">>> AM INTRAT ÎN FUNCTIA /send_mail <<<")
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    date_of_birth = request.form.get('dateOfBirth')
    nationality = request.form.get('nationality')
    address = request.form.get('address')
    motivation = request.form.get('motivation')
    hear_about = request.form.get('hearAbout')

    print(f"Received data: {first_name} {last_name}, {email}, {phone}, {date_of_birth}, {nationality}, {address}, {motivation}, {hear_about}")

    subject = "Confirmation of receipt of application – Timișoara MUN 2025 (Chairperson)"

    logo_url = "https://i.imgur.com/5w8IKVn.png"

    html_body = f"""
    <p>Dear {first_name},</p>

<p>Thank you for your interest in the Timișoara Model United Nations – First Edition.</p>

<p>We appreciate your support and enthusiasm for our event. Registration will be done on our MyMUN page:</p>

<p><a href="https://mymun.com/conferences/timisoaramun-2025" target="_blank">https://mymun.com/conferences/timisoaramun-2025</a></p>

<p>We look forward to seeing you in Timișoara!</p>

<p>With respect,<br>
Dragoș Bârlădianu<br>
Secretary General – TimișoaraMUN<br>
<a href="mailto:dragos@timisoara-mun.ro">dragos@timisoara-mun.ro</a><br>
+40&nbsp;724&nbsp;994&nbsp;673</p>

<p><img src="{logo_url}" alt="TimisoaraMUN Logo" style="max-width:200px;"></p>

`


    """

    # Trimitem email-ul prin MailerSend
    MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')  # sau direct cheia aici pt test
    test = "mlsn.b526d831333db80088c8d61a049e2249def3d83da981c12099f84031d8a65782"

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {
            "email": "noreply@timisoara-mun.ro",
            "name": "TimisoaraMUN"
        },
        "to": [
            {
                "email": email,
                "name": f"{first_name} {last_name}"
            }
        ],
        "subject": subject,
        "html": html_body
    }

    response = requests.post("https://api.mailersend.com/v1/email", json=data, headers=headers)

    if response.status_code == 202:
        flash('Application received! A confirmation email has been sent.', 'success')
    else:
        print(f"MailerSend Error: {response.text}")
        flash('There was an error with your registration. Please try again later.', 'error')

    return redirect(url_for('chairperson'))



@app.route('/send_contact_mail', methods=['POST'])
def send_contact_mail():
    print(">>> AM INTRAT ÎN FUNCTIA /send_contact_mail <<<")
    
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    print(f"Received data: {name}, {email}, {subject}, {message}")

    subject_final = f"[Contact Form] {subject if subject else 'No Subject'}"
    
    html_body = f"""
    <p>New message received from contact form:</p>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Subject:</strong> {subject}</p>
    <p><strong>Message:</strong><br>{message}</p>
    """

    MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')  # sau cheia ta direct pt test

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {
            "email": "noreply@timisoara-mun.ro",
            "name": "TimisoaraMUN Contact Form"
        },
        "to": [
            {
                "email": "chairperson.registration@timisoara-mun.ro@gmail.com",
                "name": "TimisoaraMUN Team"
            }
        ],
        "subject": subject_final,
        "html": html_body
    }

    response = requests.post("https://api.mailersend.com/v1/email", json=data, headers=headers)

    print(response.status_code)
    print(response.text)

    if response.status_code == 202:
        flash('Your message has been successfully sent!', 'success')
        print('merge')
    else:
        flash('There was an error sending your message. Please try again later.', 'error')

    return redirect(url_for('contact'))




 
@app.route("/contact")
def contact():
    return render_template('contact.html')


# ---------------------------------------- MAIL INSCRIERI ----------------------------------------


# ---------------------------------------- PAGINI ----------------------------------------


@app.route("/staff")
def staff():
    return render_template('staff.html')

@app.route("/organizing-team")
def org():
    return render_template('org.html')

@app.route('/parteners')
def parteneri():
    return render_template('parteneri.html')


@app.route("/committees/<comitet>")
def comitete(comitet):
    if comitet == "ICJ":
        size = "Size: 20 delegates"
        poza = url_for('static', filename='img/icj.png')
        comitet_name = "ICJ"
        textcomitet = """The International Court of Justice (ICJ), also known as the World Court, is the principal judicial
organ of the United Nations. Established in 1945 by the UN Charter and seated in The Hague,
Netherlands, the ICJ settles legal disputes between states and gives advisory opinions on legal
questions referred to it by authorized UN organs and specialized agencies.

Unlike other UN committees, the ICJ is not a forum for diplomatic negotiation but a legal body
that operates based on international law, treaties, conventions, and prior legal precedent. Its
rulings are binding for the states involved, and its work plays a vital role in the peaceful
resolution of international conflicts and the development of international law.

In a Model UN simulation, the ICJ committee challenges delegates to step into the role of
judges, advocates, or legal advisors. Participants must apply legal reasoning, build compelling
arguments, and interpret international law in resolving high-stakes cases that often involve
territorial disputes, human rights violations, state responsibility, or breaches of international
treaties.

The ICJ encourages critical thinking, precision in legal language, and a strong understanding of
precedent. Delegates are expected to research thoroughly, collaborate constructively, and
deliver judgments that reflect the principles of justice, neutrality, and the rule of law."""

    elif comitet == "UNSC":
        size = "Size: 25 delegates"
        poza = url_for('static', filename='img/unsc.png')
        comitet_name = "UNSC"
        textcomitet = """The United Nations Security Council (UNSC) is the principal organ of the UN responsible for
maintaining international peace and security. Composed of 15 member states – 5 permanent
(the United States, the United Kingdom, France, Russia and China) and 10 non-permanent
members – the UNSC has the authority to adopt binding resolutions, impose sanctions and
authorize peacekeeping operations or military interventions.

The UNSC is characterized by a high level of diplomatic complexity, being the only UN
structure whose decisions are binding on member states. Over time, it has been the scene of
intense debates related to international conflicts, threats to global security, terrorism and
nuclear non-proliferation.

Participants involved in a UNSC simulation must respond quickly to international crises,
collaborate effectively under pressure and navigate the delicate dynamics of the veto power
exercised by permanent members. It is a framework that encourages active diplomacy, strategic
decision-making, and in-depth understanding of international relations."""

    elif comitet == "UNHRC":
        size = "Size: 35 delegates"
        poza = url_for('static', filename='img/unhrc.png')
        comitet_name = "UNHRC"
        textcomitet = """The United Nations Human Rights Council (UNHRC) is an intergovernmental body responsible
for promoting and protecting fundamental human rights worldwide. Created in 2006, the
UNHRC is composed of 47 member states elected by the UN General Assembly and is
headquartered in Geneva, Switzerland.

The UNHRC addresses a wide range of issues, from discrimination and freedom of expression to
crimes against humanity, forced migration, violence against minorities and the rights of the
child. Through mechanisms such as the Universal Periodic Review (UPR) or special procedures,
this body assesses the situations of member states and issues recommendations with the aim
of preventing and correcting abuses.

Participating in a UNHRC simulation involves balancing a commitment to universal human
rights values ​​with the political and cultural interests of the state being represented. Delegates
must thoroughly research the international legal framework, propose equitable resolutions and
promote solutions based on dialogue, cooperation and mutual respect."""

    elif comitet == "ECOFIN":
        size = "Size: 30 delegates"
        poza = url_for('static', filename='img/ecofin.png')
        comitet_name = "ECOFIN"
        textcomitet = """The Economic and Financial Affairs Committee (ECOFIN) is the second main committee of the
United Nations General Assembly and its main objective is to analyse and debate global
economic issues and issues related to sustainable and financial development. ECOFIN deals
with topics such as international trade, economic crises, fiscal policies, sustainable
development, poverty eradication, external debt and international economic cooperation.

This framework provides the opportunity for member states to formulate proposals that can
contribute to creating a fairer and more stable global economic system. Although the
resolutions adopted by ECOFIN are not binding, they reflect international consensus and can
influence decisions taken by other international financial bodies or institutions.

Participation in an ECOFIN simulation requires a good understanding of global economic
relations, international cooperation mechanisms and the social implications of financial
policies. Delegates must combine economic analysis with diplomacy to develop balanced and
feasible solutions."""

    elif comitet == "SOCHUM":
        size = "Size: 30 delegates"
        poza = url_for('static', filename='img/sochum.png')
        comitet_name = "SOCHUM"
        textcomitet = """The Social, Humanitarian and Cultural Committee (SOCHUM) is the third main committee of the
United Nations General Assembly and aims to promote fundamental human rights, civil
liberties and social justice at the global level. SOCHUM addresses issues such as the protection
of minorities, combating discrimination, the situation of refugees, freedom of religion and
expression, and the impact of conflict on civilians.

SOCHUM frequently collaborates with bodies such as the Office of the UN High Commissioner
for Human Rights (OHCHR) or the Committee on the Elimination of Racial Discrimination
(CERD), contributing through resolutions and recommendations to the development of
international human rights norms.

Participants in a SOCHUM simulation must balance moral and ethical principles with the
geopolitical and cultural interests of the state they represent. Delegates are challenged to find
realistic solutions to complex humanitarian problems while maintaining a diplomatic and
socially sensitive approach."""

    elif comitet == "CRISIS":
        size = "Size: 20 delegates"
        poza = url_for('static', filename='img/CRISIS.png')
        comitet_name = "CRISIS"
        textcomitet = """The CRISIS Committee is a fast paced body, envisioned to be a high stakes political simulation, based on a historical scenario. Unlike traditional committees, CRISIS operates in real time, allowing delegates to respond to rapidly evolving situations, through directives and personal actions. Delegates take the roles of individuals, such as heads of states, generals, or advisors, and aim to achieve their individual goals, sometimes through unorthodox ways.
"""
    
    elif comitet == "C-24":
        size = "Size: 25 delegates"
        poza = url_for('static', filename='img/C24.png')
        comitet_name = "C-24"
        textcomitet = """The Special Committee on Decolonization, also known as C-24, was established in 1961 by the UN General Assembly to monitor the implementation of the 1960 Declaration on the Granting of Independence to Colonial Countries and Peoples. It is responsible for supporting the self-determination and independence of Non-Self-Governing Territories (NSGTs). C-24 examines political, social, and economic developments in these territories, encourages dialogue with administering powers, and promotes decolonization in accordance with international law.
"""
    
    elif comitet == "Military Tribunal":
        size = "Size: 20 delegates"
        poza = url_for('static', filename='img/MC.png')
        comitet_name = "Military Tribunal"
        textcomitet = """The Military Tribunal on the Dakota Trials is a specialized judicial body simulating the aftermath of the United States-Dakota War of 1862, focusing on the controversial military commission that sentenced over 300 Dakota men to death, most being later pardoned by President Abraham Lincoln. This tribunal explores topics such as ethics in war, indigenous rights and accountability. Delegates, simulating judges, prosecutors and generals in this war tribunal will analyze evidence, cross examine witnesses, and apply the law of that time. This committee provides an important perspective on the justice and moral conflict of this case."""

    elif comitet == "UNODC":
        size = "Size: 25 delegates"
        poza = url_for('static', filename='img/UNODC.png')
        comitet_name = "UNODC"
        textcomitet = """United Nations Office on Drugs and Crime (UNODC)
The United Nations Office on Drugs and Crime is a specialized UN agency that leads international efforts to combat illicit drugs, organized crime, terrorism, and corruption. Established in 1997 and headquartered in Vienna, Austria, UNODC works with member states to strengthen legal frameworks, support criminal justice systems, and promote international cooperation. It provides research, policy guidance, and technical assistance in areas such as drug prevention, trafficking, human rights, and anti-corruption."""

    elif comitet == "OHCHR":
        size = "Size: 25 delegates"
        poza = url_for('static', filename='img/OHCHR.png')
        comitet_name = "OHCHR"
        textcomitet = """The Office of the High Commissioner for Human Rights (OHCHR) is the principal United Nations entity responsible for promoting and protecting human rights globally. Established in 1993 following the Vienna World Conference on Human Rights, OHCHR leads international efforts to uphold the Universal Declaration of Human Rights and other international human rights instruments. Headquartered in Geneva, OHCHR monitors human rights situations, provides technical assistance to states, supports human rights mechanisms such as the Human Rights Council and treaty bodies, and advocates for accountability, equality, and the rule of law."""

    elif comitet == "WHO":
        size = "Size: 30 delegates"
        poza = url_for('static', filename='img/who.png')
        comitet_name = "WHO"
        textcomitet = """The World Health Organization (WHO) is the specialized agency of the United Nations
responsible for coordinating international efforts in the field of public health. Established in
1948, WHO’s primary objective is to achieve the highest attainable standard of health for all
people by preventing disease, promoting health, and ensuring equitable access to quality
health services.

The organization addresses a wide range of topics, from combating pandemics, infectious
diseases, and health crises to mental health, nutrition, access to vaccines, health systems, and
global public health policies.

Participants in a WHO simulation must propose effective and sustainable solutions to global
health challenges, based on scientific research, international collaboration, and inclusive
policies. Delegates will negotiate policies that meet both immediate needs and long-term
health goals, taking into account the balance between resources, ethics, and human rights."""
    elif comitet == "DISEC":
            poza = url_for('static', filename='img/who.png')
            size = "Size: 25 delegates"
            comitet_name = "DISEC"
            textcomitet = """The Disarmament and International Security Committee (DISEC) is the First Committee of the
United Nations General Assembly and is tasked with addressing issues related to global peace,
international security, and disarmament. DISEC provides a platform for member states to
debate and develop solutions to some of the most pressing threats to global stability, ranging
from nuclear proliferation to the illicit arms trade and regional conflicts.

As a beginner/intermediate committee, DISEC at TimișoaraMUN is designed to welcome both
newcomers and delegates with some MUN experience. It offers a dynamic yet approachable
environment where participants can:

    Learn and practice formal UN procedures

    Develop public speaking and negotiation skills

    Engage in diplomatic dialogue and strategic alliances

    Collaborate on realistic and impactful resolutions

Chairs will guide delegates throughout the sessions, ensuring procedural clarity and
encouraging inclusive, productive debate.

Whether you're just stepping into the world of Model UN or building upon previous experience,
DISEC is the ideal space to sharpen your diplomatic instincts and contribute to global peace
efforts."""
    else:
        return redirect(url_for('error'))

    

    return render_template("comitete.html", comitet=comitet, comitet_name = comitet_name, textcomitet = textcomitet, poza=poza, size=size)


@app.route("/chairperson-registration")
def chairperson():
    return render_template("chairmen.html")
@app.route("/delegates-registration")
def delegates():
    return render_template("delegates-registration.html")

@app.route("/FAQ")
def faq():
    return render_template("faq.html")

@app.route("/terms")
def terms():
    return render_template("policies.html")

@app.route('/error')
def error():
    return render_template('error.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route('/whoarewe')
def we():
    return render_template('whowe.html')

@app.route('/chairpersons')
def chair():
    return render_template('totichair.html')

@app.route('/advisors')
def advisors():

    return render_template('advisors.html')

@app.route('/events')
def events():

    return render_template('events.html')

@app.route('/privacy-terms.html')
def policies():
    return render_template('privacy-terms.html')
# ---------------------------------------- PAGINI END ----------------------------------------


# ---------------------------------------- ADMIN PANEL ----------------------------------------

@app.route('/adminboard')
@login_required
def adminboard():
    registrations = Registration.query.order_by(Registration.data.desc()).all()

    total = len(registrations)
    confirmati = len([r for r in registrations if r.status.lower() == 'confirmat'])
    in_asteptare = len([r for r in registrations if r.status.lower() == 'în așteptare'])
    comitete = 7

    return render_template(
        'admin/adminboard.html',
        registrations=registrations,
        total=total,
        confirmati=confirmati,
        in_asteptare=in_asteptare,
        comitete=comitete
    )

@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('loginstaff'))

@app.route('/loginstaffmuntm', methods=['GET', 'POST'])
def loginstaff():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('adminboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('loginstaff'))

    return render_template("login.html")

@app.route('/add-delegate', methods=['POST'])
def add_delegate():
    nume = request.form.get('nume')
    email = request.form.get('email')
    comitet = request.form.get('comitet')
    status = request.form.get('status')
    
    new_registration = Registration(
        nume=nume,
        email=email,
        comitet=comitet,
        status=status
    )

    db.session.add(new_registration)
    db.session.commit()

    return redirect(url_for('adminboard'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_delegate(id):
    reg = Registration.query.get_or_404(id)
    db.session.delete(reg)
    db.session.commit()
    return redirect(url_for('adminboard'))

# ---------------------------------------- ADMIN PANEL ----------------------------------------




if __name__ == '__main__':
    with app.app_context():  
        db.create_all()

    app.run(port=5050, debug=True)