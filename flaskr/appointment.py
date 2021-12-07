from flask import request, Blueprint, Response
from flaskr.db import get_db
import json
import datetime

bp = Blueprint('appointment', __name__)

@bp.route('/appointments', methods=['GET'])
def get_appointments():
    if (get_request_malformed(request)):
        return Response("{'error':'user id missing or malformed'}", status=400, mimetype='application/json')
    db = get_db()
    user_id = request.args['user_id']
    appointments = []
    rows = db.execute(
        'SELECT appointment_date, appointment_time '
        'FROM appointment WHERE user_id = (?)',
        (user_id,),
    ).fetchall()
    for row in rows:
        appointments.append(
            {
                "date": row["appointment_date"],
                "time": row["appointment_time"],
            }
        )
    return {
        "user_id": user_id,
        "appointments": appointments
    }

def get_request_malformed(request):
    return 'user_id' not in request.args

@bp.route('/create', methods=['POST'])
def create_appointment():
    if (post_request_malformed(request)):
        return Response("{'error':'post request inputs malformed'}", status=400, mimetype='application/json')
    db = get_db()
    user_id = request.json['user_id']
    appointment_datetime = datetime.datetime.fromtimestamp(request.json['datetime'])
    appointment_date = appointment_datetime.strftime('%Y-%m-%d')
    appointment_time = appointment_datetime.strftime('%H:%M')
    if (not check_no_appointment_on_date(db, user_id, appointment_date)):
        return Response("{'error':'user already has appointment that day'}", status=400, mimetype='application/json')
    if (not check_appointment_time_on_half_hour(appointment_datetime)):
        return Response("{'error':'appointment start time not available'}", status=400, mimetype='application/json')
    db.execute(
        "INSERT INTO appointment (user_id, appointment_date, appointment_time) VALUES (?, ?, ?)",
        (user_id, appointment_date, appointment_time),
    ).fetchone()
    db.commit()
    return {
        "user_id": user_id,
        "appointment": {
            "date": appointment_date,
            "time": appointment_time
        }
    }

def post_request_malformed(request):
    if ('user_id' not in request.json or 'datetime' not in request.json):
        return True
    return False

def check_no_appointment_on_date(db, user_id, appointment_date):
    existing_appointment_num = db.execute(
        'SELECT COUNT(*)'
        'FROM appointment WHERE user_id = (?) AND appointment_date = (?)',
        (user_id,appointment_date,),
    ).fetchone()[0]
    return existing_appointment_num == 0

def check_appointment_time_on_half_hour(appointment_datetime):
    minute = appointment_datetime.minute
    return minute == 0 or minute == 30