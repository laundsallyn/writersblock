# Assume that nytimes/fetched/bestseller-lists/**/*.json
# contains JSON files

import json
import os
import sys
from glob import glob
from os import makedirs
from os.path import join
from os.path import sep, realpath
from time import sleep
import csv

from scraper.goodreads.fetch.book_fetch import fetch_book_ids as apifetchbookids
from scraper.goodreads.fetch.book_fetch import fetch_work_ids as apifetchworkids

MAX_BATCH_SIZE = 100

uppath = lambda _path, n: sep.join(_path.split(sep)[:-n])
flaskapp_path = uppath(__file__, 3)
data_root = realpath(join(flaskapp_path, 'data'))

#IN_DATA_DIR = join(flaskapp_path, 'nytimes', 'data', 'fetched', 'bestseller-lists')
IN_DATA_DIR = join(flaskapp_path, 'goodreads', 'data')

INPUT_DATA = join(IN_DATA_DIR, 'ISBN2GRbid.csv')
OUTPUT_FILENAME = join(IN_DATA_DIR, 'BID2WID.csv')
#OUTPUT_DIR = join('data', 'goodreads', 'fetched')

def gather_unique_isbns(input_dir=INPUT_DATA):
    input_filenames = glob(join(input_dir, '**', '*.json'))

    isbns = []
    for fname in input_filenames:
        with open(fname, 'r') as rf:
            booksdata = json.load(rf)['results']['books']
        isbns.extend([b['primary_isbn13'] for b in booksdata])

    uniq_isbns = list(set(isbns))
    return uniq_isbns


def gather_unique_bids(input_dir=INPUT_DATA):

    gids = []
    with open(INPUT_DATA, 'rt') as csvfile:
        isbn_gid = csv.reader(csvfile, delimiter=',')

        for isbn, bid in isbn_gid:
            if bid:
                gids.append(bid)

    uniq_bids = list(set(gids))
    return uniq_bids


def batch_fetch_book_ids(apikey, isbn_numbers):

    batch_nums = range(0, len(isbns), MAX_BATCH_SIZE)
    isbnbatches = [isbns[i:i + MAX_BATCH_SIZE] for i in batch_nums]
    for batchnum in range(0, len(isbns), MAX_BATCH_SIZE):
        # create a subslice of the list
        batch = isbns[batchnum:batchnum + MAX_BATCH_SIZE]
        resp = apifetchbookids(apikey, batch)
        yield (batch, resp)


def batch_fetch_work_ids(apikey, book_ids):
    # isbnbatches = [book_ids[i:i + MAX_BATCH_SIZE] for i in range(0, len(book_ids), MAX_BATCH_SIZE)]

    return (
        (book_ids[batchnum:batchnum + MAX_BATCH_SIZE], apifetchworkids(apikey, book_ids[batchnum:batchnum + MAX_BATCH_SIZE]))
        for batchnum in range(0, len(book_ids), MAX_BATCH_SIZE)
    )


if __name__ == '__main__':
    apikey = os.environ.get("GR_KEY")

    #makedirs(OUTPUT_DIR, exist_ok=True)
    print(INPUT_DATA)
    book_ids = gather_unique_bids(INPUT_DATA)
    print(len(book_ids), 'unique book_ids')

    print(OUTPUT_FILENAME)

    if input("OK?") != 'Y': sys.exit()
    wf = open(OUTPUT_FILENAME, 'w')
    for i, (batch, resp) in enumerate(batch_fetch_work_ids(apikey, book_ids)):

        #gr_ids = resp.text.split(',')
        print('Batch number:', i, 'results:', len(resp))

        for line in [','.join(z) for z in zip(batch, resp)]:
            print(line)
            wf.write(line + '\n')
        sleep(2)
    print("Finished writing to", OUTPUT_FILENAME)
    wf.close()
