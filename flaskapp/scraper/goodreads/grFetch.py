import os
import pickle
import csv
import time
from os.path import realpath, join, pardir, curdir
from pathlib import Path
from pprint import PrettyPrinter

import requests

import scraper.shared.clients as clients
import scraper.shared.resources as resources
from pandas import DataFrame as DF


class GRClient(clients.BaseClient):
    class Meta:
        name = 'NYT Books API'
        base_url = 'http://api.nytimes.com/svc/books/v3/lists'
        resources = (NamesResource, ListResource, RankHistoryResource)
        client_key = "NYT_KEY"



pp = PrettyPrinter(indent=2)

p = Path.cwd().parent.joinpath('goodreads', 'data')
PATH = realpath(join(pardir, 'goodreads', 'data'))
# IN_FILE = realpath(join(PATH, 'ISBN2GRbid.csv'))
IN_FILE = realpath(join(PATH, 'ids.csv'))

OUTPUT_FILENAME = join(curdir, 'data', 'BID2WID.csv')
print(PATH)
print(IN_FILE)

grc = GRClient(clients.BaseClient)

gr_books = {}
gr_authors = {}
gr_series_book = {}
gr_series_author = {}
gr_series = {}

MAX_BATCH_SIZE = 100
API_ENDPOINT = 'https://www.goodreads.com/book'



def fetch_wids(api_key, bids):
    """
    arguments:
        `api_key` is Goodreads API key
        `isbns` is either a sequence of isbns string; or a comma-delimited string

    returns:
        A requests.Response object...
            let the calling user decide what to extract from it
    """
    api_key = os.environ.get("GR_KEY")
    if type(bids) is str:
        bidtxt = bids
    else:
        bidtxt = ','.join(str(i) for i in bids)
    url = API_ENDPOINT + '/id_to_work_id'
    params = {'key': api_key, 'id': bidtxt}
    return requests.get(url, params)


def batch_fetch_work_ids(book_ids):
    # isbnbatches = [book_ids[i:i + MAX_BATCH_SIZE] for i in range(0, len(book_ids), MAX_BATCH_SIZE)]

    return (
        (book_ids[batchnum:batchnum + MAX_BATCH_SIZE], fetch_wids(book_ids[batchnum:batchnum + MAX_BATCH_SIZE]))
        for batchnum in range(0, len(book_ids), MAX_BATCH_SIZE)
    )

with open(IN_FILE, 'rt') as csvfile:
    isbn_gid = csv.reader(csvfile, delimiter=',', quotechar='|')
    unmatched_isbn = []
    isbn2bid = []
    bids = []
    for isbn, gid in isbn_gid:
        if not gid:
            unmatched_isbn.append(isbn)
            continue

        isbn2bid.append({isbn: gid})
        bids.append(gid)
        book = grc.book(book_id=gid)
        series_wks = book.series_works
        if series_wks:
            swid = []
            sid = []
            for k, v in series_wks.items():
                if type(v) == list:
                    for e in v:
                        swid.append(e['id'])
                        sid.append(e['series']['id'])
                else:
                    swid.append(v['id'])
                    sid.append(v['series']['id'])

                print("swid", swid)
                print("sid", sid)
                pp.pprint(v)
                data_dict = dict(
                    isbn=book.isbn13,
                    gr_id=book.gid,
                    work_id=book.work_id,
                    series_work_id=swid,
                    sid=sid,
                    title=book.title,
                    publisher=book.publisher,
                    gr_page=book.link,
                    img=book.image_url,
                    description=book.description,
                    num_pg=book.num_pages,
                    pub_date=book.publication_date,
                    rating_avg=book.average_rating,
                    rating_dist=book.rating_dist,
                    format=book.format,
                    authors=book.authors
                )

                gr_books[gid] = data_dict
                gr_series_book[book.gid] = dict(sid=sid, work_id=book.work_id, series_work_id=swid)

                # gr_series_author[sid] = book.authors.pop()

                # print(data_dict['series_id'], "\t\t\t", data_dict['title'])

        with open(OUTPUT_FILENAME, 'w') as wf:
            bid2wid = []
            for i, (batch, resp) in enumerate(batch_fetch_work_ids(list(set(bids)))):
                gr_ids = resp.text.split(',')
                print('Batch number:', i, 'results:', len(gr_ids))

                for line in [','.join(z) for z in zip(batch, gr_ids)]:
                    print(line)
                    bid, wid = line.split()
                    bid2wid.append({bid: wid})

                    wf.write(line + '\n')
                time.sleep(2)
            print("Finished writing to", OUTPUT_FILENAME)

with open('isbn2bid', 'w') as f:
    pickle.dump(isbn2bid, f)

with open('bid2wid', 'w') as f:
    pickle.dump(bid2wid, f)

with open("unmatched_isbn.csv", 'wt') as csvfile:
    isbn_gid = csv.writer(unmatched_isbn, delimiter=',')


pickle.dump(obj=gr_books,
            file=open(join(PATH, 'gr_books.p'), 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)

# pickle.dump(obj=gr_series_author,
#            file=open(join(PATH, 'gr_series_author.p'), 'wb'),
#            protocol=pickle.HIGHEST_PROTOCOL)

pickle.dump(obj=gr_series_book,
            file=open(join(PATH, 'gr_series_book.p'), 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
"""
df = DF.from_csv(IN_FILE)
for sid in df['wid']:
    series = grc.series(series_id=sid)
    data_dict = dict(
        sid=series.sid,
        title=series.series_title,
        num_books=series.series_works_cnt,
        desc=series.series_desc,
        note=series.note,
        numbered=series.is_numbered
    )
    gr_series[sid] = data_dict
    #print(data_dict['sid'], "\t\t\t", data_dict['title'])


#pickle.dump(obj=gr_series, file=open(join(PATH, 'gr_series.p'), 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


for k, v in gr_series_author.items():
    # print(k, v)
    # pp.pprint(v)
    author = grc.find_author(author_name=v)
    # pp.pprint(author)
    data_dict = dict(
            aid=author.gid,
            about=author.about,
            gender=author.gender,
            birth_dt=author.born_at,
            death_dt=author.died_at,
            hometown=author.hometown,
            influences=author.influences,
            works_cnt=author.works_count,
            img=author.image_url,
            link=author.link,
    )
    gr_authors[author.gid] = data_dict



pickle.dump(obj=gr_authors,
            file=open(join(PATH, 'gr_authors.p'), 'wb'),
            protocol=pickle.HIGHEST_PROTOCOL)
"""
