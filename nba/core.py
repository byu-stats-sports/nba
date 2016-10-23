import nba.downloader
import nba.model


def add(season):
    nba.model.create_tables()
    #  nba.model.Team.add(nba.downloader.fetch_teams(season))
    #  nba.model.Player.add(nba.downloader.fetch_players(season))
    nba.model.TeamRoster.add(nba.downloader.fetch_team_rosters(season))
