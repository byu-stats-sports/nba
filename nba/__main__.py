#!/usr/bin/env python

"""The main entry point. Invoke as `nba` or `python -m nba`.

"""

from __future__ import print_function
from datetime import datetime, date
import argparse
import logging
import nba
import nba.model
import nba.core
from collections import namedtuple



def _log_level(verbosity_count):
    log_level = logging.WARNING
    if verbosity_count and verbosity_count is 1:
        log_level = logging.INFO
    elif verbosity_count and verbosity_count > 1:
        log_level = logging.DEBUG
    return log_level


# TODO: add support for more flexible date parsing
#       https://github.com/dateutil/dateutil/
#       https://github.com/scrapinghub/dateparser
def _valid_date(date, date_format="%m/%d/%Y"):
    """Ensures a valid date.

    Args:
        date (str): The date in the form specified in `date_format`.
        date_format (str): The date format to parse `date` according to.

    Returns:
        datetime: The date object.

    Raises:
        argparse.ArgumentTypeError: If the date cannot be parsed according to
            the specified format.
    """
    try:
        return datetime.strptime(date, date_format)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def _valid_date_range(s):
    """Ensure a valid date range.

    Args:
        s (str): A date range or single date in the form `date1-date2`

    Returns:
        (datetime, datetime): The start & end dates or (start, start).

    Raises:
        argparse.ArgumentTypeError: If either date is not valid or if date(s)
            cannot be inferred according to the above format.
    """
    dates = []
    for date in s.split('-'):
        dates.append(_valid_date(date))
    if len(dates) is 2:
        start = dates[0]
        end = dates[1]
    elif len(dates) is 1:
        start = end = dates[0]
    else:
        msg = "Not a valid date range or date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    return (start, end)

def _split_season(season):
    # NOTE: assumes 4 digit years...
    if not '-' in season or not len(season) == 7:
        msg = 'Season must be of the form: {}'.format(nba.CURRENT_SEASON)
        raise argparse.ArgumentTypeError(msg)
    start_year = int(season.split('-')[0])
    end_year = start_year + 1
    return (start_year, end_year)

def _valid_season(s=nba.CURRENT_SEASON):
    Season = namedtuple('Season', ['raw', 'start_year', 'end_year'])
    return Season(s, *_split_season(s))

def parse_args():
    """Parse and validate command line arguments.
    """
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(prog='nba',
                                     description='Manage nba statistics.',
                                     formatter_class=formatter)
    
    parser.add_argument('-V', '--version', action='version', 
                        version='%(prog)s {0}'.format(nba.__version__))

    dt = datetime.now()
    today = dt.strftime('%m/%d/%Y')
    parser.add_argument('-d', '--date', action='store', type=_valid_date_range,
                        default=today,
                        help='dash separated date range '
                             'or single date')
    
    season_example = nba.CURRENT_SEASON
    parser.add_argument('-s', '--season', action='store', type=_valid_season,
                    help='dash separated year range '
                         '(example: {0})'.format(season_example))

    parser.add_argument("-v", "--verbose", action="count",
                        help="increase output verbosity")

    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s')
    logging.getLogger().setLevel(_log_level(args.verbose))
    
    start, end = args.date
    nba.core.update(args.season)
    
if __name__ == '__main__':
    import sys
    sys.exit(main())
