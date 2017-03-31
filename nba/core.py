import nba.downloader
import nba.model


def update(season, should_update=True):
    teams = nba.downloader.fetch_teams()
    players = nba.downloader.fetch_players()
    team_rosters = nba.downloader.fetch_team_rosters()
    games, inactive_players_games = nba.downloader.fetch_games(season) #took out season to try and see if it works. 
    players_games = nba.downloader.fetch_games_by_player(season)
    
    if should_update:
        nba.model.create_tables()
        nba.model.update(nba.model.Players, players)
        nba.model.update(nba.model.Teams, teams)
        nba.model.update(nba.model.TeamRosters, team_rosters)
        nba.model.update(nba.model.Games, games)
        nba.model.update(nba.model.GamesMissedByPlayer, inactive_players_games)
        nba.model.update(nba.model.GamesByPlayer, players_games)
