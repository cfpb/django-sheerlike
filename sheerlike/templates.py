import datetime
from dateutil import parser
from pytz import timezone


def date_formatter(value, format="%Y-%m-%d", tz='America/New_York'):
    if type(value) not in [datetime.datetime, datetime.date]:
        value = parser.parse(value, default=datetime.datetime.today().replace(day=1))
    naive = value.replace(tzinfo=None)
    dt = timezone(tz).localize(naive)

    return dt.strftime(format)
