import pprint

from player_info import Player_Info


class Activity(object):
    """Creates Activity object."""

    def __init__(self, data):
        """Initialize Activity object."""

        # this is where we will store the activity
        self.recent_activity = []

        # individual activity fields
        self.actingAsTeamOwner = None
        self.activityType = None
        self.batchProcessed = None
        self.bidAmount = None
        self.byLM = None
        self.date = None
        self.dateAccepted = None
        self.dateModified = None
        self.dateProposed = None
        self.dateToProcess = None
        self.parentPendingMoveBatchId = None
        self.pendingMoveBatchId = None
        self.pendingMoveItems = None

        # fetch activity for league_id/year/cookies
        self._fetch_activity(data)

    def _fetch_activity(self, data):
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data)

        self.events = []
        self.actingAsTeamOwner = data['actingAsTeamOwner']
        self.activityType = int(data['activityType'])
        self.batchProcessed = data['batchProcessed']
        self.bidAmount = data['bidAmount']
        self.byLM = data['byLM']
        self.date = data['date']
        self.dateAccepted = data['dateAccepted']
        self.dateModified = data['dateModified']
        self.dateProposed = data['dateProposed']
        self.dateToProcess = data['dateToProcess']
        self.parentPendingMoveBatchId = data['parentPendingMoveBatchId']
        self.pendingMoveBatchId = data['pendingMoveBatchId']
        self.pendingMoveItems = data['pendingMoveItems']

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint()
        # pp.pprint(data)

        # if self.pendingMoveItems:
        #     self.pendingMoveItemsHuman = self.get_human(self.pendingMoveItems)
            # print(self.pendingMoveItemsHuman)
        self.pendingMoveItemsCount = len(self.pendingMoveItems)
        # {   'draftOverallSelection': 0,
        #                             'fromSlotCategoryId': 1001,
        #                             'fromTeamId': -1,
        #                             'keeper': False,
        #                             'moveTypeId': 2,
        #                             'playerId': 60008,
        #                             'rating': 0,
        #                             'toSlotCategoryId': 20,
        #                             'toTeamId': 5},
        #
        self.proposingTeamId = data['proposingTeamId']
        self.proposingUserProfileId = data['proposingUserProfileId']
        self.rating = data['rating']
        self.scoringPeriodToProcess = data['scoringPeriodToProcess']
        self.skipTransactionCounters = data['skipTransactionCounters']
        self.statusId = data['statusId']
        self.teamsAcceptedTrade = data['teamsAcceptedTrade']
        self.teamsInvolved = data['teamsInvolved']
        self.teamsVotedApproveTrade = data['teamsVotedApproveTrade']
        self.teamsVotedVetoTrade = data['teamsVotedVetoTrade']
        self.tradeProposalExpirationDays = data['tradeProposalExpirationDays']
        self.transactionLogItemTypeId = data['transactionLogItemTypeId']
        self.typeId = int(data['typeId'])
        self.userProfileId = data['userProfileId']
        self.usersProtestTrade = data['usersProtestTrade']
        # self.name = data['leaguesettings']['name']
        # print("__init__ Activity object")

    def get_human(self, move_items):
        # mapping IDs/types
        move_type_map = {
            2: 'Add',
            3: 'Drop',
            5: 'Draft',
        }
        team_map = {
            1: 'Ryne',
            2: 'Morgan',
            3: 'Kenny',
            4: 'Bobby',
            5: 'Jordan',
            6: 'Cassady',
            7: 'Adam',
            8: 'Shannon',
            9: 'Cody',
            10: 'Chris',
            -1: 'FA/Waivers/Null'
        }
        roster_map = {0: 'QB', 1: 'TQB',
                      2: 'RB', 3: 'RB/WR',
                      4: 'WR', 5: 'WR/TE',
                      6: 'TE', 7: 'OP',
                      8: 'DT', 9: 'DE',
                      10: 'LB', 11: 'DL',
                      12: 'CB', 13: 'S',
                      14: 'DB', 15: 'DP',
                      16: 'D/ST', 17: 'K',
                      18: 'P', 19: 'HC',
                      20: 'BE', 21: 'IR',
                      22: '', 23: 'RB/WR/TE',
                      1001: 'FA', 1002: 'Waivers'}
        # {   'draftOverallSelection': 0,
        #                             'fromSlotCategoryId': 16,
        #                             'fromTeamId': 5,
        #                             'keeper': False,
        #                             'moveTypeId': 3,
        #                             'playerId': 60029,
        #                             'rating': 0,
        #                             'toSlotCategoryId': 1002,
        #                             'toTeamId': -1}],
        l = []
        for item in move_items:
            # print(item)
            x = {}
            x['draftOverallSelection'] = item['draftOverallSelection']
            x['fromSlotCategoryId'] = item['fromSlotCategoryId']
            x['fromTeamId'] = item['fromTeamId']
            x['keeper'] = item['keeper']
            x['moveTypeId'] = item['moveTypeId']
            x['playerId'] = item['playerId']
            x['rating'] = item['rating']
            x['toSlotCategoryId'] = item['toSlotCategoryId']
            x['toTeamId'] = item['toTeamId']
            l.append("Player: {}".format(x['playerId']))
            playa = Player_Info(x['playerId'])
            print(playa)
            l.append("moveType: {}".format(move_type_map.get(x['moveTypeId'], 'unknown ???')))
            l.append("from team [{}] to team [{}]".format(
                team_map[x['fromTeamId']],
                team_map[x['toTeamId']]))
            l.append("from slot [{}] --> [{}]".format(
                roster_map[x['fromSlotCategoryId']],
                roster_map[x['toSlotCategoryId']]))

            # print(x)
        # return '\n'.join(l)

    def __repr__(self):
        return 'Activity({0})'.format(self.transactionLogItemTypeId)

    def __str__(self):
        move_type_map = {2: 'Add', 3: 'Drop', 5: 'Draft'}
        team_map = {
            1: 'Ryne',
            2: 'Morgan',
            3: 'Kenny',
            4: 'Bobby',
            5: 'Jordan',
            6: 'Cassady',
            7: 'Adam',
            8: 'Shannon',
            9: 'Cody',
            10: 'Chris',
            -1: 'FA/Waivers/Null'
        }
        roster_map = {0: 'QB', 1: 'TQB',
                      2: 'RB', 3: 'RB/WR',
                      4: 'WR', 5: 'WR/TE',
                      6: 'TE', 7: 'OP',
                      8: 'DT', 9: 'DE',
                      10: 'LB', 11: 'DL',
                      12: 'CB', 13: 'S',
                      14: 'DB', 15: 'DP',
                      16: 'D/ST', 17: 'K',
                      18: 'P', 19: 'HC',
                      20: 'BE', 21: 'IR',
                      22: '', 23: 'RB/WR/TE',
                      1001: 'FA', 1002: 'Waivers'}
        date = self.date
        activity_type = move_type_map.get(self.activityType, 'unknown activityType???')
        teams_involved = []
        for team in self.teamsInvolved:
            teams_involved.append(team_map.get(team, 'unknown team???'))

        # include basic text for involved teams
        text = ["[{0}] Transaction [{1}] involving team {2}".format(
            date,
            activity_type,
            '/'.join(teams_involved))]
        # check for pending move items and include those too
        if self.pendingMoveItemsCount and self.pendingMoveItemsCount > 0:
            for item in self.pendingMoveItems:
                player = Player_Info(item['playerId'])
                move = 'Team {0} moved {1} [{2}] from {3} to Team {4}'.format(
                    team_map.get(item['fromTeamId'], 'unknown team'),
                    player,
                    roster_map.get(item['fromSlotCategoryId'], 'unknown fromSlotCategoryId'),
                    roster_map.get(item['toSlotCategoryId'], 'unknown toSlotCategoryId'),
                    team_map.get(item['toTeamId'], 'unknown team')
                )
                text.append('---- {0}'.format(move))

        return '\n'.join(text)

    def attr_list(self, should_print=False):
        items = self.__dict__.items()
        if should_print:
            # [print(f"attribute: {k:20s} : {v}") for k, v in items]
            for k, v in items:
                print("attribute: {0:20s} : {1}".format(k, v))
        return items
