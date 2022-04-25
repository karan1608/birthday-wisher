import requests
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import re
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPeerUser, InputPeerChannel, InputPhoneContact
from telethon import TelegramClient, sync, events

import random
import smtplib
import pandas
import datetime as dt

now = dt.datetime.now()

views = Blueprint('views', __name__)


def date_checker(date_date):
    r = re.compile('.*/.*/.*:.*')
    if r.match(date_date) is not None:
        return True
    else:
        return False


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        now = dt.datetime.now()
        data = request.form.get('note')
        email = request.form.get('note_email')
        name = request.form.get('note_name')
        date = request.form.get('note_date')
        form = request.form.get('note_form')
        if len(data) < 1:
            flash('Note is too short!', category='error')
        elif not date_checker(date):

            flash('Date format is wrong!', category='error')
        else:
            new_note = Note(data=data, email=email, name=name, date=date, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

            bday_d = int(date.split("/")[0])
            bday_m = int(date.split("/")[1])
            # print(type(bday_m), type(now.month))
            if bday_m == now.month:
                # print("m s")
                if bday_d == now.day:
                    if new_note.greet == 0:
                        #---------------------------------------------------------
                        # phone = "+919840025725"
                        # client = TelegramClient("Test", 11922065, "bd5283ce86287d62813b1ec0fef8a9ec")
                        # client.start()
                        # destination_user_username = '919840046483'
                        # entity = client.get_entity(destination_user_username)
                        # client.send_message(entity=entity, message="Hi")
                        #-----------------------------------------------------------
                        base_url = "https://api.telegram.org/bot5160337233:AAEx3Mo1MyqBYqSjwbROzmmcRrKjlB8mCmc/sendMessage"

                        parameters = {
                            "chat_id": 5003209061,
                            "text": f"Happy Birthday {name}"
                        }

                        kili = requests.get(base_url, params=parameters)

                        kili.raise_for_status()

                        print(kili.json())
                        #-----------------------------------------------------------
                        print("sending mail...")
                        my_email = "professorsergiomarquinasalva@gmail.com"
                        password = "qazwsxcde12"

                        connection = smtplib.SMTP("smtp.gmail.com")
                        connection.starttls()
                        connection.login(my_email, password)
                        connection.sendmail(from_addr=my_email, to_addrs=email,
                                            msg=f"Subject:Flask\n\nHappy Birthday {name}")
                        new_note.greet = 1
                        db.session.commit()

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
