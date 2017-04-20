import nba_py.player
import nba_py.team
import nba_py.game
import nba_py.league
import nba_py.draftcombine
import dateutil.parser
import datetime
import sys
sys.path.append('/Users/chris/Desktop/NBA Injury Data/nba')
import nba
import nba.utils
import logging
from pprint import pprint 

logger = logging.getLogger(__name__)

def fetch_players(season=None, only_current=1):
    logger.info('Downloading player data...')
    if not season:
        season = nba.utils.valid_season(nba.CURRENT_SEASON)# if the user does not specify a season, download all seasons
        only_current = 0
    draft_combine = {}# TODO: handle only_current season...
    for p in nba_py.draftcombine.DrillResults(season=season.raw).overall():
        player = {
            'bench_press': p['BENCH_PRESS'],
            'three_quarter_sprint': p['THREE_QUARTER_SPRINT'],
            'lane_agility_time': p['LANE_AGILITY_TIME'],
            'modified_lane_agility_time': p['MODIFIED_LANE_AGILITY_TIME'],
            'standing_vertical_leap': p['STANDING_VERTICAL_LEAP']
        }
        draft_combine[p['PLAYER_NAME']] = player# use dictionary to ensure uniqueness
    players = {}
    for p in nba_py.player.PlayerList(season=season.raw,
                                      only_current=only_current).info():
        if p['GAMES_PLAYED_FLAG'] is 'N':
            continue
        player = nba_py.player.PlayerSummary(p['PERSON_ID']).info()[0]
        if p['ROSTERSTATUS'] is 'Inactive':
            continue
        player_id = player['PERSON_ID']
        first_name = player['FIRST_NAME']
        last_name = player['LAST_NAME']
        player = {
            'player_id': player_id,
            'first_name': first_name,
            'last_name': last_name,
            'birthdate': dateutil.parser.parse(player['BIRTHDATE']).date(),
            'height': nba.utils.height_in_inches(player['HEIGHT'] or None),
            'weight': player['WEIGHT'] or None,
            'from_year': nba.utils.season_start(player['FROM_YEAR']),
            'to_year': nba.utils.season_end(player['TO_YEAR']),
            'position': player['POSITION'] or None,
        }
        try:# TODO: is there any better way of id than first and last name?
            player.update(draft_combine[p['DISPLAY_FIRST_LAST']])
        except:
            pass
        players[player_id] = player
    return players.values()


def fetch_teams():
    logger.info('Downloading team data...') # use dictionary to ensure uniqueness
    teams = {}
    for t in nba_py.team.TeamList().info():
        try:
            team = nba_py.team.TeamDetails(t['TEAM_ID']).background()[0]
            del(team['YEARFOUNDED'])
        except IndexError:#  historical team
            continue
        team['MIN_YEAR'] = datetime.datetime(int(t['MIN_YEAR']), 1, 1)
        team['MAX_YEAR'] = datetime.datetime(int(t['MAX_YEAR']), 1, 1)
        team = dict((k.lower(), v) for k, v in team.items())
        teams[team['team_id']] = team
    return teams.values()


def fetch_team_rosters(season=None):
    logger.info('Downloading team rosters data...')
    if not season:
        season = nba.utils.valid_season(nba.CURRENT_SEASON)# use dictionary to ensure uniqueness
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
            players[player['player']] = player
    return players.values()


def fetch_games(season=None):
    logger.info('Downloading game data...')# TODO: add points for each team?
    if not season:
        season = nba.utils.valid_season(nba.CURRENT_SEASON)
    winners = {}
    losers = {}
    games = [] #Testing games and inactive players as dicts instead to see if it works.
    inactive_players = []
    for g in nba_py.league.GameLog(season=season.raw,
                                   counter=10000000,
                                   player_or_team='T').overall():
        d = winners if g['WL']=='W' else losers
        d[g['GAME_ID']] = g['TEAM_ID'] # all matchups in season (1230 = 15 teams * 82 games)
    for game_id in winners.keys():
        game = nba_py.game.BoxscoreSummary(game_id)
        for p in game.inactive_players():
            player = {'game': int(game_id), 'player': p['PLAYER_ID']}
            inactive_players.append(player)
        game_info = game.game_info()[0]
        game_summary = game.game_summary()[0]
        game = {
            'game_id': game_id,
            'season_start': season.start,
            'season_end': season.end,
            'date': dateutil.parser.parse(game_summary['GAME_DATE_EST']).date(),
            'duration': nba.utils.duration_in_minutes(game_info['GAME_TIME']),
            'periods': game_summary['LIVE_PERIOD'],
            'attendance': game_info['ATTENDANCE'],
            'home_team': game_summary['HOME_TEAM_ID'],
            'visitor_team': game_summary['VISITOR_TEAM_ID'],
            'winner_team': winners[game_id],
            'loser_team': losers[game_id]
        }
        games.append(game)
    return (games, inactive_players)


def fetch_games_by_player(season=None):
    logger.info('Downloading game by player data...')
    if not season:
        season = nba.utils.valid_season(nba.CURRENT_SEASON)        
    games = []
    for g in nba_py.league.GameLog(season=season.raw,
                                   counter=10000000,
                                   player_or_team='P').overall():
        game = {
            'game': int(g['GAME_ID']),
            'player': int(g['PLAYER_ID']),
            'team': int(g['TEAM_ID']),
            'minutes_played': g['MIN'],
            'points': g['PTS'],
            'plus_minus': g['PLUS_MINUS'],
            'assists': g['AST'],
            'steals': g['STL'],
            'blocks': g['BLK'],
            'turnovers': g['TOV'],
            'rebounds': g['REB'],
            'offensive_rebounds': g['OREB'],
            'defensive_rebounds': g['DREB'],
            'free_throws_made': g['FTM'],
            'free_throws_attempted': g['FTA'],
            'free_throws_percentage': g['FT_PCT'],
            'field_goals_made': g['FGM'],
            'field_goals_attempted': g['FGA'],
            'field_goals_percentage': g['FG_PCT'],
            'three_point_field_goals_made': g['FG3M'],
            'three_point_field_goals_attempted': g['FG3A'],
            'three_point_field_goals_percentage': g['FG3_PCT']
        }
        games.append(game)
    return games
