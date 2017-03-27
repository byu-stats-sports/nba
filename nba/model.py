import peewee as orm
from playhouse.db_url import connect
import nba
from nba import DATABASE_URL
import logging
from pprint import pformat, pprint

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

    class Meta:
        database = db


class Players(orm.Model):
    player_id = orm.PrimaryKeyField()

    first_name = orm.CharField()
    last_name = orm.CharField()
    birthdate = orm.DateField()
    height = orm.IntegerField(null=True, help_text='height in inches')
    weight = orm.IntegerField(null=True)

    position = orm.CharField(null=True)
    from_year = orm.DateField()
    to_year = orm.DateField()

    lane_agility_time = orm.FloatField(null=True)
    modified_lane_agility_time = orm.FloatField(null=True)
    standing_vertical_leap = orm.FloatField(null=True)
    three_quarter_sprint = orm.FloatField(null=True)
    bench_press = orm.IntegerField(null=True)

    class Meta:
        database = db
        order_by = ('last_name', 'first_name', '-birthdate')


class TeamRosters(orm.Model):
    player = orm.ForeignKeyField(Players, related_name='player')
    team = orm.ForeignKeyField(Teams, related_name='team')
    season_start = orm.DateField()
    season_end = orm.DateField()

    class Meta:
        database = db
        db_table = 'team_rosters'


class Games(orm.Model):
    game_id = orm.PrimaryKeyField()
    season_start = orm.DateField()
    season_end = orm.DateField()
    date = orm.DateField()
    duration = orm.IntegerField(null=True, help_text='duration in minutes')
    periods = orm.IntegerField()
    attendance = orm.IntegerField()
    home_team = orm.ForeignKeyField(Teams, related_name='home_team')
    visitor_team = orm.ForeignKeyField(Teams, related_name='visitor_team')
    winner_team = orm.ForeignKeyField(Teams, related_name='winner_team')
    loser_team = orm.ForeignKeyField(Teams, related_name='loser_team')

    class Meta:
        database = db


class GamesByPlayer(orm.Model):
    # FIXME: deafult = 0 is default = NULL
    game = orm.ForeignKeyField(Games, related_name='game')
    player = orm.ForeignKeyField(Players, related_name='player_by_game')
    team = orm.ForeignKeyField(Teams, related_name='team_by_game')
    minutes_played = orm.IntegerField()
    points = orm.IntegerField(default=0.0)
    plus_minus = orm.IntegerField(default=0.0)
    assists = orm.IntegerField(default=0.0)
    steals = orm.IntegerField(default=0.0)
    blocks = orm.IntegerField(default=0.0)
    turnovers = orm.IntegerField(default=0.0)
    rebounds = orm.IntegerField(default=0.0)
    offensive_rebounds = orm.IntegerField(default=0.0)
    defensive_rebounds = orm.IntegerField(default=0.0)
    free_throws_made = orm.IntegerField(default=0.0)
    free_throws_attempted = orm.IntegerField(default=0.0)
    free_throws_percentage = orm.FloatField(null=True)
    field_goals_made = orm.IntegerField(default=0.0)
    field_goals_attempted = orm.IntegerField(default=0.0)
    field_goals_percentage = orm.FloatField(null=True)
    three_point_field_goals_made = orm.IntegerField(default=0.0)
    three_point_field_goals_attempted = orm.IntegerField(default=0.0)
    three_point_field_goals_percentage = orm.FloatField(null=True)
    
    class Meta:
        database = db
        db_table = 'games_by_player'


class GamesMissedByPlayer(orm.Model):
    game = orm.ForeignKeyField(Games, related_name='missed_game')
    player = orm.ForeignKeyField(Players, related_name='missed_player')
   
    class Meta:
        database = db
        db_table = 'games_missed_by_player'


def create_tables(tables=[Players, Teams, TeamRosters, Games,
                          GamesMissedByPlayer, GamesByPlayer]):
    db.create_tables(tables, safe=True)


@db.atomic()
def add(model, data):
    logger.info('Adding data to the {0} database table...'
                .format(model._meta.db_table))
    logger.debug(pformat(list(data)))
    return model.insert_many(data).execute()


@db.atomic()
def update(model, data):
    logger.info('Updating the {0} database table...'
                .format(model._meta.db_table))
    logger.debug(pformat(list(data)))
    for item in data:
        try:
            orm.InsertQuery(model, field_dict=item).upsert().execute()
        # TODO: fix IntegrityError due to `Cannot delete or update a parent row: a foreign key constraint fails`
        except orm.IntegrityError as e:
            # seems to be the only way to access e.errno
            # TODO: figure out a better way to only print when not a duplicate key
            if e.args[0] != 1062:
                logger.warning('{}: {!r}'.format(item, e))
                # raise e  # TODO: we might want to raise errors that are anything besides duplicate key errors 
