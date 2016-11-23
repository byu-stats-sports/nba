import nba
import argparse
import logging
import datetime
from collections import namedtuple


def log_level(verbosity_count):
    log_level = logging.WARNING
    if verbosity_count and verbosity_count is 1:
        log_level = logging.INFO
    elif verbosity_count and verbosity_count > 1:
        log_level = logging.DEBUG
    return log_level


# TODO: add support for more flexible date parsing
#       https://github.com/dateutil/dateutil/
#       https://github.com/scrapinghub/dateparser
def valid_date(date, date_format="%m/%d/%Y"):
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
        return datetime.datetime.strptime(date, date_format)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def valid_date_range(s):
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
        dates.append(valid_date(date))
    if len(dates) is 2:
        start = dates[0]
        end = dates[1]
    elif len(dates) is 1:
        start = end = dates[0]
    else:
        msg = "Not a valid date range or date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    return (start, end)


def season_start(year):
    # NOTE: assumes an NBA season starts on October 1
    return datetime.datetime(year, 10, 1)


def season_end(year):
    # NOTE: assumes an NBA season ends on June 1
    return datetime.datetime(year, 6, 1)


def split_season(season):
    # NOTE: assumes 4 digit years...
    if not '-' in season or not len(season) == 7:
        msg = 'Season must be of the form: {}'.format(nba.CURRENT_SEASON)
        raise argparse.ArgumentTypeError(msg)
    start_year = int(season.split('-')[0])
    end_year = start_year + 1
    return (season_start(start_year), season_end(end_year))


def valid_season(s=nba.CURRENT_SEASON):
    Season = namedtuple('Season', ['raw', 'start', 'end'])
    return Season(s, *split_season(s))


def height_in_inches(height):
    """Convert height string to inches. (e.g. 6-9 -> 81)

    Args:
        height (str): A height in the format: ft-inches

    Returns:
        inches: The height in inches.
    """
    try:
        inches = int(height)
    except (ValueError, TypeError):
        inches = None
        height = str(height).split('-')
        if len(height) is 2:
            try:
                inches = (int(height[0]) * 12) + int(height[1])
            except:
                inches = None
    return inches


def duration_in_minutes(duration):
    """Convert duration string to minutes. (e.g. 1:09 -> 69)

    Args:
        duration (str): A duration in the format: hh:mm

    Returns:
        minutes: The duration in minutes.
    """
    minutes = None
    duration = str(duration).split(':')
    if len(duration) is 2:
        try:
            minutes = (int(duration[0]) * 60) + int(duration[1])
        except:
            minutes = None
    return minutes

