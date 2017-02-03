import calendar
import json
import os
import sys  # for the exit
import time
from datetime import datetime
from os import makedirs
from os.path import join, realpath

import requests
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, WEEKLY

API_ENDPOINT = "http://api.nytimes.com/svc/books/v3"
LISTS_PATH = "/lists/{weekdate}/{listname}.json"
NAMES_PATH = "/lists/names.json"

api_key = os.environ.get('NYT_KEY')
nyt_data_root = realpath(join(os.pardir, 'data', 'fetched'))
list_root = realpath(join(nyt_data_root, 'bestseller-lists'))


def fetch_list_names(session):
    """
    Retrieve list of best-seller lists for further queries
    """
    names_list = realpath(join(nyt_data_root, 'list_names.json'))
    if os.path.isfile(names_list):
        with open(names_list, "r") as fp:
            return json.load(fp)

    params = {'api-key': api_key}
    url = API_ENDPOINT + NAMES_PATH
    resp = session.get(url, params=params)

    if resp.status_code != 200:
        print("Exiting!\nStatus code is:\t{}\nText dump:\t{}"
              .format(resp.status_code, resp.text))
        sys.exit()

    lists = resp.json()['results']

    with open(names_list, 'w') as fp:
        json.dump(lists, fp)

    return lists


def fetch_list(session, list_name, date):
    """
    Retrieve a rank list for a given best-sellers list and week

    @precondition api_key: is NYT API key

    @param session: python requests Session for repeated calls to this api
    @param list_name: canonical name of a best-sellers list,
            e.g. 'combined-print-and-e-book-fiction'
    @param date: "YYYY-MM-DD" format (e.g. '2015-01-01')

    @return: Response object
    """
    params = {'api-key': api_key}
    url = API_ENDPOINT + LISTS_PATH.format(weekdate=date, listname=list_name)
    print("Fetching URL:\t", url)

    resp = session.get(url, params=params)
    if(int(resp.headers["X-RateLimit-Remaining-second"]) < 3):
        time.sleep(1)
    print("{}/{} daily requests remaining".format(resp.headers["X-RateLimit-Remaining-day"], resp.headers["X-RateLimit-Limit-day"]))

    if resp.status_code != 200:
        print("Exiting!\nStatus code is:\t{}\nText dump:\t{}"
              .format(resp.status_code, resp.text))
        sys.exit()

    fname = join(savetodir, '{date}.json'.format(date=dt))
    with open(fname, 'w') as fp:
        json.dump(resp.json(), fp)


def generate_weekdate_strings(fp, ymd_start, ymd_end):
    existing = [os.path.splitext(os.path.basename(fn))[0] for fn in os.listdir(fp)]

    two_years = datetime.now() + relativedelta(weekday=calendar.WEDNESDAY) - relativedelta(years=1)

    def dt_format(dt):
        try:
            return datetime.strptime(dt, '%Y-%m-%d')
        except TypeError:
            return dt.strftime('%Y-%m-%d')

    dx = max(dt_format(ymd_start), two_years)
    dy = dt_format(ymd_end)

    date_iterator = rrule(cache=True, freq=WEEKLY, dtstart=dx, until=dy)
    return [
        dt_format(dt)
        for dt in date_iterator
        if not any(abs(relativedelta(dt1=parse(e), dt2=dt).days) > 2 for e in existing)
    ]


if __name__ == '__main__':
    if not api_key:
        raise ValueError('api_key NYT_KEY not detected')

    s = requests.Session()
    for l in fetch_list_names(s):
        listname = l['list_name_encoded']
        beg_date = l['oldest_published_date']
        end_date = l['newest_published_date']

        # verify or create dir
        savetodir = realpath(join(list_root, listname))
        makedirs(savetodir, exist_ok=True)

        # generate dates
        weekdates = generate_weekdate_strings(savetodir, beg_date, end_date)

        if not len(weekdates): print(listname, "\n"); continue
        print("Best-seller list:\t{list}\n"
              "( {total} ) Weeks\t--\tFrom: {beg}\tTo: {end}\n"
              "Saving to:{dir}\n\n".format(list=listname,
                                           total=len(weekdates),
                                           beg=weekdates[0],
                                           end=weekdates[-1],
                                           dir=savetodir))

        if input("OK?") != 'Y': continue

        for i, dt in enumerate(weekdates):
            print(dt, '({ith}/{count})\n'.format(ith=i + 1, count=len(weekdates)))
            fetch_list(session=s, date=dt, list_name=listname)
