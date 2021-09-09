"""Pull recent activity from ESPN public/private league."""
import os
import smtplib
from datetime import datetime, timedelta
from dateutil import parser
import requests

# import events object which holds Activity objects
from events import Events


def fetch_team_map(league_id, year, cookies):
    """Fetch team abbrev + names from leagueSettings."""
    # fetch teams from ENDPOINT+leagueSettings
    ENDPOINT = "http://games.espn.com/ffl/api/v2/"

    # set parameters
    params = {
        'leagueId': league_id,
        'seasonId': year
    }

    # send GET request
    r = requests.get('{0}leagueSettings'.format(ENDPOINT), params=params, cookies=cookies)
    status = r.status_code

    # if not successful, raise an exception
    if status != 200:
        raise Exception('[script.py] Requests status != 200. It is: {0}'.format(status))

    # store response
    data = r.json()
    teams = data['leaguesettings']['teams']

    # iterate through each team and fill the team_map
    team_map = {}
    for team in teams:
        team_id = int(team)
        team_abbrev = teams[team]['teamAbbrev']
        team_owner = "{0} {1}".format(teams[team]['owners'][0].get('firstName', ''),
                                      teams[team]['owners'][0].get('lastName', ''))
        # print("team_id: {} team_abbrev: {} team_owner: {}".format(team_id, team_abbrev, team_owner))
        team_map[team_id] = "{} [{}]".format(team_abbrev.upper(), team_owner.title())

    # be sure to include the FA/waivers team
    team_map[-1] = 'FA/Waivers/Null'

    # print(team_map)
    return team_map


def main():
    """Check each league for recent activity and send a text message."""
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

        # fetch teams in leagueId
        team_map = fetch_team_map(league_id, year, cookies)

        # create Events object (holds Activity) object and return recent activity
        recent_activity = Events(league_id, year, team_map, cookies).recent_activity

        # iterate through each activity event
        for a in recent_activity:
            # convert activity date (iso format) to datetime
            activity_date = parser.parse(a.date)
            # make date naive
            activity_date = activity_date.replace(tzinfo=None)
            # if date of transaction is less than timedelta threshold, send message
            if activity_date >= current_dt - timedelta(minutes=threshold):
                print("Activity date [{0}] is >= current date [{1}] - threshold [{2} minutes]".format(
                    activity_date, current_dt, threshold
                ))
                # check if text_msg is empty
                if not text_msg:
                    text_msg.append("League {0}".format(league_map.get(league_id, '???')))

                # append str representation to text_msg
                text_msg.append(str(a))

                print("Appending text_msg:\n")
                print(a)
            # else:
            #     print(a)
            #     break

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


if __name__ == "__main__":
    main()
