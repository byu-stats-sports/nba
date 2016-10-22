import peewee as orm
import nba
from nba import DATABASE_CONNECTION as db

class BaseModel(orm.Model):
    class Meta:
        database = db

class Team(BaseModel):
    team_id = orm.PrimaryKeyField()
    abbreviation = orm.CharField()
    nickname = orm.CharField()
    yearfounded = orm.DateField()
    city = orm.CharField()
    arena = orm.CharField()
    arenacapacity = orm.IntegerField()
    owner = orm.CharField()
    generalmanager = orm.CharField()
    headcoach = orm.CharField()
    dleagueaffiliation = orm.TextField()

class Player(BaseModel):
    player_id = orm.PrimaryKeyField()
    team = orm.ForeignKeyField(Team, to_field='team_id', related_name='team')

    first_name = orm.CharField()
    last_name = orm.CharField()
    birthdate = orm.DateField()
    height = orm.CharField(null=True)
    weight = orm.IntegerField(null=True)

    position = orm.CharField()
    #  rosterstatus = orm.CharField()
    #  jersey = orm.IntegerField() 
    from_year = orm.DateField()
    to_year = orm.DateField()

    lane_agility_time = orm.DecimalField(null=True)
    modified_lane_agility_time = orm.DecimalField(null=True)
    standing_vertical_leap = orm.DecimalField(null=True)
    three_quarter_sprint = orm.DecimalField(null=True)
    bench_press = orm.IntegerField(null=True)

