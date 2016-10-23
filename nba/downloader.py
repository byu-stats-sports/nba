import nba_py.player
import nba_py.team
import dateutil.parser
import datetime
import nba
import nba.utils
import logging

logger = logging.getLogger(__name__)

def fetch_players(season=None, only_current=1):
    logger.info('Downloading player data...')
    if not season:
        # if the user does not specify a season download all seasons
        season = nba.CURRENT_SEASON
        only_current = 0
    else:
        season = season.raw

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
            'first_name': player['FIRST_NAME'], 
            'last_name': player['LAST_NAME'], 
            'birthdate': dateutil.parser.parse(player['BIRTHDATE']).date(),
            'height': player['HEIGHT'] or None,
            'weight': player['WEIGHT'] or None, 
            'from_year': nba.utils.season_start(player['FROM_YEAR']),
            'to_year': nba.utils.season_end(player['TO_YEAR']),
            'position': player['POSITION'] or None,
        }

        logger.info(player) 
        players[player_id] = player

    return players.values()


def fetch_teams(season=None):
    logger.info('Downloading team data...')
    if not season:
        season = nba.CURRENT_SEASON
    else:
        season = season.raw

    # use dictionary to ensure uniqueness
    teams = {}
    for t in nba_py.team.TeamList().info():
        try:
            team = nba_py.team.TeamDetails(t['TEAM_ID']).background()[0]
            del(team['YEARFOUNDED'])
        except IndexError:
            #  historical team
            continue

        team['MIN_YEAR'] = datetime.datetime(int(t['MIN_YEAR']), 1, 1)
        team['MAX_YEAR'] = datetime.datetime(int(t['MAX_YEAR']), 1, 1)
        team = dict((k.lower(), v) for k, v in team.items())
        logger.info(team) 
        teams[team['team_id']] = team

    return teams.values()


def fetch_team_rosters(season=nba.utils.valid_season(nba.CURRENT_SEASON)):
    # use dictionary to ensure uniqueness
    players = {}
    for t in nba_py.team.TeamList().info():
        for p in nba_py.team.TeamCommonRoster(season=season.raw,
                                              team_id=t['TEAM_ID']).roster():
            player = {
                'player': p['PLAYER_ID'],
                'team': t['TEAM_ID'],
                'season_start': season.start,
                'season_end': season.end
            }
            logger.info(player) 
            players[player['player']] = player

    return players.values()
            


