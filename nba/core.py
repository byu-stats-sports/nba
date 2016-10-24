import nba.downloader
import nba.model


def add(season):
    nba.model.create_tables()
    nba.model.Teams.add(nba.downloader.fetch_teams())
    nba.model.Players.add(nba.downloader.fetch_players(season))
    nba.model.TeamRosters.add(nba.downloader.fetch_team_rosters(season))
    games, inactive_players_games = nba.downloader.fetch_games(season)
    nba.model.Games.add(games)
    nba.model.GamesMissedByPlayer.add(inactive_players_games)
