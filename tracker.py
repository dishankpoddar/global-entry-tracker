import datetime
import requests
import os
from config import (
    SENDGRID_API_KEY, SENDGRID_TEMPLATE_ID, 
    FROM_EMAIL, TO_EMAILS,
    LOCATION_CODES, CODE_DATES
)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

"""
Use this link to find  the codes of the locations you are interested in
https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry
"""
def log(*args):
    log_message = '\t'.join(args)
    print(log_message)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'tracker.log')
    with open(file_path, 'a') as logfile:
        logfile.write(f'{log_message}\n')

def send_dynamic_email(appointments):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAILS)
    message.dynamic_template_data = {
        'subject': 'New Appointment Available for Global Entry',
        'appointments': appointments,
    }
    message.template_id = SENDGRID_TEMPLATE_ID
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        log('Email Sent!')
    except Exception as e:
        log(f'Error: {e}')


def get_appointments(location_codes, code_dates):
    appointments = []

    for location_code, appointment_location in location_codes.items():
        url = f'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&locationId={location_code}&minimum=1'
        response = requests.get(url)
        location_appointments = response.json()
        if len(location_appointments) > 0:
            earliest_appointment = location_appointments[0]
            appointment_date_string = earliest_appointment['startTimestamp']
            appointment_date = datetime.datetime.strptime(appointment_date_string, '%Y-%m-%dT%H:%M')
            code_date_max = datetime.datetime.strptime(code_dates[location_code], '%Y-%m-%dT%H:%M')
            if appointment_date < code_date_max:
                appointment = f'Appointment available on {appointment_date_string} at {appointment_location}'
                appointments.append(appointment)
    return appointments

if __name__ == '__main__':
    log_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
    log(log_time, 'New Attempt')

    location_codes = LOCATION_CODES
    code_dates = CODE_DATES
    
    appointments = get_appointments(location_codes, code_dates)
    if appointments:
        log(*appointments)
        send_dynamic_email(appointments)
    else:
        log('No Appointments available')
