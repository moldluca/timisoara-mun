from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from models import db, Registration


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




@app.route('/')
def home():
    return render_template('index.html')

# ---------------------------------------- MAIL INSCRIERI ----------------------------------------

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

    logo_url = "https://i.imgur.com/u6P2Tk7.png"  # ← aici pui linkul tău direct către imagine

    html_body = f"""
    <p>Dear {first_name},</p>

    <p>Thank you for completing the application form on our website and for your interest in the position of Chairperson within Timișoara Model United Nations – First Edition.</p>

    <p>This email confirms that we have received your application. In order for your registration to be complete, you must also complete the final registration form, available at the link: 
    <a href="https://tally.so/r/nWB2lL" target="_blank">https://tally.so/r/nWB2lL</a></p>

    <p>Only candidates who have completed both forms, the one on the website and the registration form, will be considered for selection.</p>

    <p>Please note that only selected candidates will receive an email confirming their selection, along with all the necessary information regarding participation in the event. All details regarding the event and program will be announced soon.</p>

    <p>The event will take place in Timișoara, between 18–20 August 2025, in several representative locations in the city.</p>

    <p>For questions related to the selection process or the responsibilities of the Chairperson role, please write to us at: <a href="mailto:chairperson.registration@timisoara-mun.ro">chairperson.registration@timisoara-mun.ro</a></p>

    <p>For technical assistance or problems related to the form: <a href="mailto:erol@timisoara-mun.ro">erol@timisoara-mun.ro</a></p>

    <p>Thank you for your interest and involvement!</p>

    <p>Best regards,<br>
    TimișoaraMUN 2025 Registration Team</p>

    <p><img src="{logo_url}" alt="TimisoaraMUN Logo" style="max-width:200px;"></p>
    """

    msg = Message(
        subject=subject,
        recipients=[email],
        html=html_body
    )

    try:
        mail.send(msg)
        flash('Application received! A confirmation email has been sent.', 'success')
        return redirect(url_for('chairmen'))
    except Exception as e:
        print(f"Error: {e}")
        flash('There was an error with your registration. Please try again later.', 'error')
        return redirect(url_for('chairmen'))



# ---------------------------------------- MAIL INSCRIERI ----------------------------------------


# ---------------------------------------- PAGINI ----------------------------------------
# 

@app.route("/committees/<comitet>")
def comitete(comitet):
    if comitet == "ICJ":
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

    elif comitet == "WHO":
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
    else:
        return redirect(url_for('error'))

    

    return render_template("comitete.html", comitet=comitet, comitet_name = comitet_name, textcomitet = textcomitet)


@app.route("/chairmen-registration")
def chairmen():
    return render_template("chairmen.html")

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

# ---------------------------------------- PAGINI END ----------------------------------------


# ---------------------------------------- ADMIN PANEL ----------------------------------------

@app.route('/adminboard')
def adminboard():
    registrations = Registration.query.order_by(Registration.data.desc()).all()

    total = len(registrations)
    confirmati = len([r for r in registrations if r.status.lower() == 'confirmat'])
    in_asteptare = len([r for r in registrations if r.status.lower() == 'în așteptare'])
    comitete = len(set([r.comitet for r in registrations]))

    return render_template(
        'admin/adminboard.html',
        registrations=registrations,
        total=total,
        confirmati=confirmati,
        in_asteptare=in_asteptare,
        comitete=comitete
    )

@app.route('/loginstaffmuntm')
def loginstaff():
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

    app.run(debug=True)