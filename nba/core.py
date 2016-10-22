import nba_py.player
import nba_py.team
import logging 
from nba.model import Player, Team
import dateutil.parser
import datetime
from nba import DATABASE_CONNECTION
import nba

class Downloader:
    def players(self, season=None, only_current=1):
        logging.info('Downloading player data...')
        if not season:
            # if the user does not specify a season download all seasons
            season = nba.CURRENT_SEASON
            only_current = 0

        # use dictionary to ensure uniqueness
        players = {}

        for p in nba_py.player.PlayerList(season=season, 
                                          only_current=only_current).info():
            if p['GAMES_PLAYED_FLAG'] is 'N':
                continue

            player = nba_py.player.PlayerSummary(p['PERSON_ID']).info()[0]

            if p['ROSTERSTATUS'] is 'Inactive':
                continue 

            player_id = player['PERSON_ID']
            # NOTE: assumes an NBA starts on October 1 and ends June 1
            player = {
                'player_id': player_id,
                'team': player['TEAM_ID'], 
                'first_name': player['FIRST_NAME'], 
                'last_name': player['LAST_NAME'], 
                'birthdate': dateutil.parser.parse(player['BIRTHDATE']).date(),
                'height': player['HEIGHT'] or None,
                'weight': player['WEIGHT'] or None, 
                'from_year': datetime.datetime(player['FROM_YEAR'], 10, 1),
                'to_year': datetime.datetime(player['TO_YEAR'], 6, 1),
                'position': player['POSITION'], 
            }

            logging.info(player) 
            players[player_id] = player

        return players.values()

    def teams(self, season=None):
        logging.info('Downloading team data...')
        if not season:
            season = nba.CURRENT_SEASON

        # use dictionary to ensure uniqueness
        teams = {}
        for t in nba_py.team.TeamList().info():
            try:
                team = nba_py.team.TeamDetails(t['TEAM_ID']).background()[0]
            except IndexError:
                logging.warning(t)
                continue 

            team = dict((k.lower(), v) for k, v in team.items())
            logging.info(team) 
            team['yearfounded'] = datetime.datetime(team['yearfounded'], 1, 1)
            teams[team['team_id']] = team

        return teams.values()


class Database:
    def __init__(self, connection):
        self.connection = connection
        self.connection.create_tables([Team, Player], safe=True)

    def commit(self, stmt):
        with self.connection.atomic() as transaction:
            try:
                stmt.execute()
            except Exception as e:
                self.connection.rollback()
                logging.error(e)

def update(season):
    download = Downloader() 
    database = Database(DATABASE_CONNECTION)
    
    database.commit(Team.insert_many(download.teams(season)))
    database.commit(Player.insert_many(download.players(season)))
