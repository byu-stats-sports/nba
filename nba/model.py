import peewee as orm
from playhouse.db_url import connect
import nba
from nba import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

db = connect(DATABASE_URL)


class Team(orm.Model):
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
        return Team.insert_many(teams).execute()

    class Meta:
        database = db


class Player(orm.Model):
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
        return Player.insert_many(players).execute()

    class Meta:
        database = db
        order_by = ('last_name', 'first_name', '-birthdate')


class TeamRoster(orm.Model):
    player = orm.ForeignKeyField(Player, to_field='player_id', related_name='player')
    team = orm.ForeignKeyField(Team, to_field='team_id', related_name='team')
    season_start = orm.DateField()
    season_end = orm.DateField()
    
    @db.atomic()
    def add(players):
        return TeamRoster.insert_many(players).execute()

    class Meta:
        database = db
        db_table = 'team_roster'


def create_tables():
    db.create_tables([Team, Player, TeamRoster], safe=True)
