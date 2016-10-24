import peewee as orm
from playhouse.db_url import connect
import nba
from nba import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

db = connect(DATABASE_URL)


class Teams(orm.Model):
    team_id = orm.PrimaryKeyField()
    abbreviation = orm.CharField(null=True)
    nickname = orm.CharField(null=True)
    min_year = orm.DateField()
    max_year = orm.DateField()
    city = orm.CharField(null=True)
    arena = orm.CharField(null=True)
    arenacapacity = orm.IntegerField(null=True)
    owner = orm.CharField(null=True)
    generalmanager = orm.CharField(null=True)
    headcoach = orm.CharField(null=True)
    dleagueaffiliation = orm.TextField(null=True)

    @db.atomic()
    def add(teams):
        return Teams.insert_many(teams).execute()

    class Meta:
        database = db


class Players(orm.Model):
    player_id = orm.PrimaryKeyField()

    first_name = orm.CharField()
    last_name = orm.CharField()
    birthdate = orm.DateField()
    height = orm.CharField(null=True)
    weight = orm.IntegerField(null=True)

    position = orm.CharField(null=True)
    from_year = orm.DateField()
    to_year = orm.DateField()

    lane_agility_time = orm.DecimalField(null=True)
    modified_lane_agility_time = orm.DecimalField(null=True)
    standing_vertical_leap = orm.DecimalField(null=True)
    three_quarter_sprint = orm.DecimalField(null=True)
    bench_press = orm.IntegerField(null=True)

    @db.atomic()
    def add(players):
        return Players.insert_many(players).execute()

    class Meta:
        database = db
        order_by = ('last_name', 'first_name', '-birthdate')


class TeamRosters(orm.Model):
    player = orm.ForeignKeyField(Players, related_name='player')
    team = orm.ForeignKeyField(Teams, related_name='team')
    season_start = orm.DateField()
    season_end = orm.DateField()

    @db.atomic()
    def add(players):
        return TeamRosters.insert_many(players).execute()

    class Meta:
        database = db
        db_table = 'team_rosters'


class Games(orm.Model):
    game_id = orm.PrimaryKeyField()
    season_start = orm.DateField()
    season_end = orm.DateField()
    date = orm.DateField()
    #  time
    duration = orm.IntegerField(verbose_name='duration in minutes')
    periods = orm.IntegerField()
    attendance = orm.IntegerField()
    home_team = orm.ForeignKeyField(Teams, related_name='home_team')
    visitor_team = orm.ForeignKeyField(Teams, related_name='visitor_team')
    winner_team = orm.ForeignKeyField(Teams, related_name='winner_team')
    loser_team = orm.ForeignKeyField(Teams, related_name='loser_team')

    @db.atomic()
    def add(games):
        return Games.insert_many(games).execute()

    class Meta:
        database = db

class GamesMissedByPlayer(orm.Model):
    game = orm.ForeignKeyField(Games, related_name='game')
    player = orm.ForeignKeyField(Players, related_name='missed_player')

    @db.atomic()
    def add(games):
        return GamesMissedByPlayer.insert_many(games).execute()

    class Meta:
        database = db
        db_table = 'games_missed_by_player'

def create_tables(tables=[Teams, Players, TeamRosters, Games,
                          GamesMissedByPlayer]):
    db.create_tables(tables, safe=True)
