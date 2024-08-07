import datetime
import requests

"""
Use this link to find  the codes of the locations you are interested in
https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry
"""

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
    location_codes = {
        5360: 'Las Vegas Enrollment Center',
        # 5447: 'Sanford Global Entry Enrollment Center',
        # 5380: 'Orlando International Airport',
        # 8020: 'Tampa Enrollment Center',
    }

    code_dates = {
        5360: '2024-11-10T00:00',
        # 5447: '10/10/2024',
        # 5380: '10/10/2024',
        # 8020: '10/10/2024',
    }

    appointments = get_appointments(location_codes, code_dates)