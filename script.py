"""Pull recent activity from ESPN public/private league."""
import os
import smtplib
from datetime import datetime, timedelta
from dateutil import parser

# import events object which holds Acitivyt objects
from events import Events


def main():

    # pull espn_s1 and swid cookies from .env file (or in the environment somehow)
    espn_s2 = os.environ['espn_s2']
    swid = os.environ['swid']
    email = os.environ['email']
    app_pw = os.environ['app_pw']
    phone = os.environ['phone']

    # setup league IDs
    league_ids = [427822, 294822, 153494]
    league_map = {
        427822: '10-man Keeper',
        294822: '12-man Re-draft',
        153494: '12-man Dynasty'
    }
    year = 2018

    # get/set cookies
    cookies = None
    if espn_s2 and swid:
        cookies = {
            'espn_s2': espn_s2,
            'SWID': swid
        }

    # get current time in UTC
    current_dt = datetime.utcnow()

    # set threshold (minutes) for timedelta
    threshold = 10

    # check transaction in each league
    for league_id in league_ids:
        text_msg = []
        print("League {0}".format(league_map.get(league_id, '???')))

        # create Events object (holds Activity) object and return recent activity
        recent_activity = Events(league_id, year, cookies).recent_activity

        # iterate through each activity event
        for a in recent_activity:
            # convert activity date (iso format) to datetime
            activity_date = parser.parse(a.date)
            # make date naive
            activity_date = activity_date.replace(tzinfo=None)
            print("Difference between {} [now] and {} is {}".format(
                current_dt,
                activity_date,
                current_dt - activity_date
            ))
            # if date of transaction is less than timedelta threshold, send message
            if activity_date >= current_dt - timedelta(minutes=threshold):
                print("It is >=")
                # check if text_msg is empty
                if len(text_msg) == 0:
                    text_msg.append("League {0}".format(league_map.get(league_id, '???')))

                # append str representation to text_msg
                text_msg.append(str(a))

                print("Appending text_msg:")
                print(a)
            else:
                print("Nope. It is <")
                print(a)

        # send email
        # TODO only create SMTP connect if message to send
        if text_msg:
            # if there is a message to send, connect to gmail
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, app_pw)
            # print("Message that would have been sent")
            # print('\n'.join(text_msg))
            server.sendmail(email, phone, '\n'.join(text_msg))
            server.quit()

        else:
            print("No transactions within threshold")


if __name__ == "__main__":
    main()
