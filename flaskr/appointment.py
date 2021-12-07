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
    user_id = int(request.args['user_id'])
    appointments = []
    rows = db.execute(
        'SELECT appointment_date, appointment_time '
        'FROM appointment WHERE user_id = (?)',
        (user_id,),
    ).fetchall()

    """Deconstruct Row type into JSON map"""
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
    """Check that User ID exists in the query parameters and is expected format"""
    return ('user_id' not in request.args 
    or not request.args['user_id'].isdigit() 
    or int(request.args['user_id']) <= 0)

@bp.route('/create', methods=['POST'])
def create_appointment():
    if (post_request_malformed(request)):
        return Response("{'error':'post request inputs malformed'}", status=400, mimetype='application/json')
    db = get_db()
    user_id = int(request.json['user_id'])

    """Parse datetime into separate components for date and time"""
    appointment_datetime = datetime.datetime.fromtimestamp(int(request.json['datetime']))
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
    """Check that request type and inputs are as expected"""
    if (not request.is_json or 'user_id' not in request.json or 'datetime' not in request.json):
        return True
    user_id = request.json['user_id']
    datetime = request.json['datetime']

    """Check that User ID and DateTime are valid inputs"""
    user_id_valid = (isinstance(user_id, int) or (isinstance(user_id, str) and user_id.isdigit())) and int(user_id) > 0
    datetime_valid = isinstance(datetime, int) or (isinstance(datetime, str) and datetime.isdigit())
    if (user_id_valid and datetime_valid):
        return False
    return True

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