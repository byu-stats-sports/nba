"""
nba - a CLI to manage BYU Sports Statistics NBA data.
"""
import os
import nba_py
__author__ = 'William Myers'
__version__ = '0.0.1'
__licence__ = 'GPLv3+'

#Comment this database_url line out when running code. 
DATABASE_URL = os.environ['BYU_NBA_DATABASE_URL']
CURRENT_SEASON = nba_py.constants.CURRENT_SEASON
