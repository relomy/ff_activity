import requests

from activity import Activity


class Events:
    """Creates Events object."""

    def __init__(self, leagueId, year, team_map, cookies=None):
        # arguments
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.league_id = leagueId
        self.year = year
        self.team_map = team_map
        self.cookies = cookies

        # store Activity objects in here
        self.recent_activity = []

        # fetch activity from ENDPOINT
        self._fetch_activity()

    def _fetch_activity(self):
        params = {
            'leagueId': self.league_id,
            'seasonId': self.year
        }

        # GET recentActivity with params and cookies
        r = requests.get('{0}recentActivity'.format(self.ENDPOINT), params=params, cookies=self.cookies)
        status = r.status_code
        data = r.json()

        # if not successful, raise an exception
        if status != 200:
            raise Exception('[script.py] Requests status != 200. It is: {0}'.format(status))

        # get all items
        fetched_activity = data['items']

        for single in fetched_activity:
            a = Activity(single, self.team_map)
            self.recent_activity.append(a)
