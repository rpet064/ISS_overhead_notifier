import requests
import datetime as dt
import smtplib
import time

# variables
MY_LAT = -37
MY_LONG = 175
FORMATTED = 0
MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"


def iss_overhead():
    # ISS API request
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    # lat and long float so can be subtracted later
    iss_lat = round(float(iss_data["iss_position"]["latitude"]))
    iss_long = round(float(iss_data["iss_position"]["longitude"]))
    # check if iss distance is close to me
    if -5 < (iss_lat - MY_LAT) > 5 and -5 < (iss_long - MY_LONG) > 5:
        return True


def is_night():
    parameters = {"lat": MY_LAT,
                  "long": MY_LONG,
                  "formatted": FORMATTED
                  }
    # sunrise/sunset API request
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    # auckland sunrise & sunset hour
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split(":")[0])
    # current hour now
    now = dt.datetime.now()
    hour_now = now.hour
    # check if weather is dark
    if hour_now > sunset_hour or hour_now < sunrise_hour:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg="subject:Look up!\n\nThe ISS is about to fly overhead"
                                )
