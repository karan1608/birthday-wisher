import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import smtplib
import pandas
import datetime as dt
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPeerUser, InputPeerChannel, InputPhoneContact
from telethon import TelegramClient, sync, events


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    now = dt.datetime.now()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                print(user.notes)
                for note in user.notes:
                    # print("1")
                    print(note.greet)
                    mail = note.email
                    name = note.name
                    bday = note.date
                    bday_d = int(bday.split("/")[0])
                    bday_m = int(bday.split("/")[1])
                    # print(type(bday_m), type(now.month))
                    if bday_m == now.month:
                        # print("m s")
                        if bday_d == now.day:
                            if note.greet == 0:
                                #---------------------------------------------------------------------------
                                # phone = "+919840025725"
                                # client = TelegramClient("Test", 11922065, "bd5283ce86287d62813b1ec0fef8a9ec")
                                # client.start()
                                # destination_user_username = '919840046483'
                                # entity = client.get_entity(destination_user_username)
                                # client.send_message(entity=entity, message="Hi")
                                #---------------------------------------------------------------------------
                                base_url = "https://api.telegram.org/bot5160337233:AAEx3Mo1MyqBYqSjwbROzmmcRrKjlB8mCmc/sendMessage"

                                parameters = {
                                    "chat_id": 5003209061,
                                    "text": "Hola Amigo"
                                }

                                kili = requests.get(base_url, params=parameters)

                                kili.raise_for_status()

                                print(kili.json())
                                #---------------------------------------------------------------------------
                                print("sending mail...")
                                my_email = "professorsergiomarquinasalva@gmail.com"
                                password = "qazwsxcde12"

                                connection = smtplib.SMTP("smtp.gmail.com")
                                connection.starttls()
                                connection.login(my_email, password)
                                connection.sendmail(from_addr=my_email, to_addrs=mail,
                                                    msg=f"Subject:Flask\n\nHappy Birthday {name}")
                                note.greet = 1
                                # print(note.greet)
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
