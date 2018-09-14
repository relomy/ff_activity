"""Pull recent activity from ESPN public/private league."""
import os

from events import Events

ENDPOINT = "http://games.espn.com/ffl/api/v2/"

# pull espn_s1 and swid cookies from .env file (or in the environment somehow)
espn_s2 = os.environ['espn_s2']
swid = os.environ['swid']

league_id = 427822
year = 2018

league_ids = [427822, 294822, 153494]
league_map = {
    427822: '10-man Keeper',
    294822: '12-man Re-draft',
    153494: '12-man Dynasty'
}

cookies = None
if espn_s2 and swid:
    cookies = {
        'espn_s2': espn_s2,
        'SWID': swid
    }

for league_id in [427822]:
    print("League {0}".format(league_map.get(league_id, '???')))
    year = 2018
    params = {
        'leagueId': league_id,
        'seasonId': year
    }

    recent_activity = Events(league_id, year, cookies).recent_activity

    for a in recent_activity:
        print(a)
