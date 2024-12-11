import requests
import time
import sys
from datetime import datetime, timedelta
from twilioNotifier import sendSMS
from twitterNotifier import postTweet
from telegramNotifier import sendMessage

# API URL
APPOINTMENTS_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={}&minimum=1"

# List of Global Entry locations
# Full list: https://ttp.cbp.dhs.gov/schedulerapi/slots/asLocations?limit=100
LOCATION_IDS = {
    "Blaine NEXUS": 5020,
    "SEAFO-Blaine": 16764
}

# How often to run this check in seconds
TIME_WAIT = 30

# Number of days into the future to look for appointments
DAYS_OUT = 4

# Dates
now = datetime.now()
future_date = now + timedelta(days=DAYS_OUT)


def check_appointments(city, id):
    url = APPOINTMENTS_URL.format(id)
    appointments = requests.get(url).json()
    return appointments

def appointment_in_timeframe(now, future_date, appointment_date):
    return now <= appointment_date <= future_date

if __name__ == "__main__":
    try:
        while True:
            for city, id in LOCATION_IDS.items():
                try:
                    appointments = check_appointments(city, id)
                except Exception as e:
                    print("Could not retrieve appointments from API")
                    continue
                if appointments:
                    appt_datetime = datetime.strptime(appointments[0]['startTimestamp'], '%Y-%m-%dT%H:%M')
                    if appointment_in_timeframe(now, future_date, appt_datetime):
                        message = "{}: Available appointment on {}".format(city, appointments[0]['startTimestamp'])
                        print(message)
                        # sendSMS(message)
                        postTweet(message)
                    else:
                        print("{}: No appointments available in {} days".format(city, DAYS_OUT))
                else:
                    print("{}: No appointments available".format(city, DAYS_OUT))
                time.sleep(1)
            time.sleep(TIME_WAIT)
    except KeyboardInterrupt:
        sys.exit(0)
    