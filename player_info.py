import requests
import pprint


class Player_Info:
    def __init__(self, player_id):
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.player_id = player_id
        self.pro_games = []
        self.status = None

        # fields
        self.serverDate = None
        self.eligibleSlotCategoryIds = None
        self.defaultPositionId = None
        self.draftRank = None
        self.droppable = None
        self.eligibleSlotCategoryIds = None
        self.first_name = None
        self.gameStarterStatus = None
        self.healthStatus = None
        self.isActive = None
        self.isIREligible = None
        self.last_name = None
        self.lastNewsDate = None
        self.lastVideoDate = None
        self.percentChange = None
        self.percentOwned = None
        self.percentStarted = None
        self.proTeamId = None
        self.sportsId = None
        self.tickerId = None
        self.universeId = None
        self.value = None

        # proTeamId map
        self.pro_team_map = {
            0: 'FA',
            1: 'ATL',
            2: 'BUF',
            3: 'CHI',
            4: 'CIN',
            5: 'CLE',
            6: 'DAL',
            7: 'DEN',
            8: 'DET',
            9: 'GB',
            10: 'TEN',
            11: 'IND',
            12: 'KC',
            13: 'OAK',
            14: 'LAR',
            15: 'MIA',
            16: 'MIN',
            17: 'NE',
            18: 'NO',
            19: 'NYG',
            20: 'NYJ',
            21: 'PHI',
            22: 'ARI',
            23: 'PIT',
            24: 'LAC',
            25: 'SF',
            26: 'SEA',
            27: 'TB',
            28: 'WSH',
            29: 'CAR',
            30: 'JAX',
            33: 'BAL',
            34: 'HOU'
        }

        self._fetch_player()

    def _fetch_player(self):
        espn_s2 = 'AEBIHfAdeVRceS6p6Ah5iWdYr7mCZyH3g7rtbSmY4v4GAgfmmiLjXC3tW1LZ%2B7n18FmawicMV0EOMi2y6nSPS77h8niR4XL7C%2BYVjXOb4MwRZFm%2FPvBPE%2B%2BgDXqJb8nTsKjDCGMaP2E0ohj%2BVmwSkmp8u87OFfc2xO5eHfCeQDs2pdSEOE3LVbIiPa%2BEBVU9TG21jH2hRWamt5lyLQwwV9zt3BfPJnuokzSwmywKjYTfiDhLq1SBSplqzpRga563AErHMmY85j8r9Zv01DUbL0Cp'
        swid = '{BF5EF061-3A31-42E0-B830-9657593EEEAF}'

        cookies = {
            'espn_s2': espn_s2,
            'SWID': swid
        }

        params = {
            'playerId': self.player_id
        }
        r = requests.get('%splayerInfo' % (self.ENDPOINT, ), params=params, cookies=cookies)
        self.status = r.status_code
        data = r.json()

        if self.status != 200:
            raise Exception('Requests status != 200. It is: {0}'.format(self.status))

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data)

        # only useful thing in metadata
        self.serverDate = data['metadata']['serverDate']
        # 'playerInfo': { 'players:' [
        playa = data['playerInfo']['players'][0]['player']
        # pp.pprint(data)
        self.eligibleSlotCategoryIds = playa['eligibleSlotCategoryIds']

        self.defaultPositionId = playa['defaultPositionId']
        self.draftRank = playa['draftRank']
        self.droppable = playa['droppable']
        self.eligibleSlotCategoryIds = playa['eligibleSlotCategoryIds']
        self.first_name = playa['firstName']
        self.gameStarterStatus = playa['gameStarterStatus']
        self.healthStatus = playa['healthStatus']
        self.isActive = playa['isActive']
        self.isIREligible = playa['isIREligible']
        self.last_name = playa['lastName']
        self.lastNewsDate = playa['lastNewsDate']
        self.lastVideoDate = playa['lastVideoDate']
        self.percentChange = playa['percentChange']
        self.percentOwned = playa['percentOwned']
        self.percentStarted = playa['percentOwned']
        self.proTeamId = playa['proTeamId']
        self.sportsId = playa['sportsId']
        self.tickerId = playa['tickerId']
        self.universeId = playa['universeId']
        self.value = playa['value']

        # use pro_team_map to map proTeamId
        self.proTeam = self.pro_team_map.get(self.proTeamId, '???')

        self.pro_games = data['playerInfo']['progames']
        # for k, v in pro_games.items():
        #     print(v)
        # print(pro_games)
        # 'percentChange': 23.76736,
        # 'percentOwned': 46.30647,
        # 'percentStarted': 41.4532,
        # 'playerId': 60008,
        # 'proTeamId': 8,
        # 'sportsId': 60008,
        # 'tickerId': 0,
        # 'universeId': 2,
        # 'value': -1}
         #                                 'rosterStatus': 0,
         #                                 'team': {   'teamAbbrev': 'FA',
         #                                             'teamId': -1,
         #                                             'teamNickname': 'Free '
         #                                                             'Agency',
         #                                             'waiverRank': 0},
         #                                 'teamId': -1,
         #                                 'watchList': False}],
         #              'progames': {   '380910008': {   'awayProTeamId': 20,
         #                                               'awayScore': 0,
         #                                               'gameDate': '2018-09-10T23:10:00.000Z',
         #                                               'gameId': 380910008,
         #                                               'homeProTeamId': 8,
         #                                               'homeScore': 0,
         #                                               'period': 0,
         #                                               'status': 1,
         #                                               'timeRemainingInPeriod': '0:00'}},
         #              'scoringPeriodId': 1}}
        # pp.pprint(data)

    def __repr__(self):
        return 'Player_Info({} {}, {})'.format(self.first_name, self.last_name, self.player_id)

    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name, self.proTeam)

    def attr_list(self, should_print=False):
        """Return (or print) the attributes associated with this classself."""
        items = self.__dict__.items()
        if should_print:
            # [print(f"attribute: {k:20s} : {v}") for k, v in items]
            for k, v in items:
                print("attribute: {0:20s} : {1}".format(k, v))
        return items
