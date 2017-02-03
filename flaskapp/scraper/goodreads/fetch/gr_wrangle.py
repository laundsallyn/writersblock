from pickle import load
from csv import reader
from os.path import realpath, join, pardir
from pathlib import Path
from pprint import PrettyPrinter
from pandas import DataFrame as DF

from flaskapp.scraper.goodreads.fetch.client import GoodreadsClient

pp = PrettyPrinter(indent=4)

# FILES = ['gr_books.p', 'gr_authors.p', 'gr_series.p', 'gr_series_author.p', 'gr_series_book.p']
FILES = ['gr_series_book.p']
OUT = 'ids.csv'
PATH = realpath(join(pardir, 'data'))
OUT_FILE = realpath(join(PATH, OUT))

for file in FILES:
    IN_FILE = realpath(join(PATH, file))
    print(IN_FILE)

    # makedirs(OUT_PATH, exist_ok=True)

    # if isfile('gr_books.p'):

    gr_data = load(open(IN_FILE, 'rb'))
    # pp.pprint(gr_data)

    df = DF.from_dict(gr_data).transpose()
    df.reset_index(inplace=True)
    df.columns = ['bid', 'swid', 'sid', 'wid']
    print(df)

    rows = []
    _ = df.apply(lambda row: [rows.append([row['bid'], row['wid'], n1, n2])
                              for n1 in row['swid']
                              for n2 in row['sid']], axis=1)
    df_new = DF(rows, columns=df.columns).set_index(['bid'])
    print(df_new)

    df_new.to_csv(OUT_FILE)

"""
    for bid, v in gr_data.items():
        for id in v.items():
            #print(v)
            if id == 'sid':
                for i, j in v.items():
                    print("\t", i, j)
        print(bid)
"""

"""
    i = 0
    # print(gr_data)
    for k, v in gr_data.items():
        # print(k, "\t", v)
        # print(k, v)
        s = v['series']
        if s:
            series_work = s['series_work']
            print(series_work['id'], "\n")
            if series_work:
                series_id = series_work['series']['id']
                print(series_id)
"""
