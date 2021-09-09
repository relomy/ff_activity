"""Pull recent activity from ESPN public/private league."""
import os
import smtplib
from datetime import datetime, timedelta
from espn_api.football import League


def main():
    """Check each league for recent activity and send a text message."""
    # pull espn_s1 and swid cookies from .env file (or in the environment somehow)
    espn_s2 = os.environ["espn_s2"]
    swid = os.environ["swid"]
    email = os.environ["email"]
    app_pw = os.environ["app_pw"]
    phone = os.environ["phone"]

    # setup league IDs
    # league_ids = [427822, 294822, 153494]
    league_ids = [427822]
    league_map = {
        427822: "10-man Keeper",
        294822: "12-man Re-draft",
        153494: "12-man Dynasty",
    }
    year = 2021

    # get current time in UTC
    current_dt = datetime.utcnow()

    # set threshold (minutes) for timedelta
    threshold = 10

    # check transaction in each league
    for league_id in league_ids:
        text_msg = []

        # fetch league and recent activity
        league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        recent_activity = league.recent_activity()

        # fetch teams in leagueId
        # team_map = fetch_team_map(league_id, year, cookies)

        # create Events object (holds Activity) object and return recent activity
        # recent_activity = Events(league_id, year, team_map, cookies).recent_activity

        # iterate through each activity event
        for activity in recent_activity:
            # convert activity date (iso format) to datetime
            activity_date = datetime.fromtimestamp(activity.date / 1000)
            # make date naive
            activity_date = activity_date.replace(tzinfo=None)

            # if date of transaction is less than timedelta threshold, send message
            if activity_date >= current_dt - timedelta(minutes=threshold):
                print(
                    "Activity date [{0}] is >= current date [{1}] - threshold [{2} minutes]".format(
                        activity_date, current_dt, threshold
                    )
                )
                # check if text_msg is empty
                if not text_msg:
                    text_msg.append(
                        "League {0}".format(league_map.get(league_id, "???"))
                    )

                current_activity = activity.actions[0]
                team = current_activity[0]
                action = current_activity[1]
                player = current_activity[2]
                msg = str(team) + " " + action + " " + str(player)

                # append str representation to text_msg
                text_msg.append(msg)

                print("Appending text_msg:\n")
                print(activity)

        # send email
        if text_msg:
            # if there is a message to send, connect to gmail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, app_pw)
            # print("Message that would have been sent")
            # print('\n'.join(text_msg))
            server.sendmail(email, phone, "\n".join(text_msg))
            server.quit()


if __name__ == "__main__":
    main()
