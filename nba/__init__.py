"""
nba - a CLI to manage BYU Sports Statistics NBA data.
"""
from playhouse.db_url import connect
import os

__author__ = 'William Myers'
__version__ = '0.0.1'
__licence__ = 'GPLv3+'

DATABASE_URL = os.environ.get('BYU_NBA_DATABASE_URL')
DATABASE_CONNECTION = connect(DATABASE_URL)
#  CURRENT_SEASON = nba_py.constants.CURRENT_SEASON
CURRENT_SEASON = '2015-16'
