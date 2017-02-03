import csv
import json
import os
from glob import glob
from os import makedirs, listdir, pardir
from os.path import join, sep, realpath

nyt_data_root = realpath(join(pardir, 'data'))
IN_DATA_DIR = join(nyt_data_root, 'fetched', 'bestseller-lists')
OUT_DATA_DIR = join(nyt_data_root, 'wrangled', 'listings')
makedirs(OUT_DATA_DIR, exist_ok=True)

BASIC_BOOK_HEADERS = ['primary_isbn13', 'weeks_on_list', 'publisher', "author", "amazon_product_url", "book_image", "description",]
FULL_HEADERS = BASIC_BOOK_HEADERS + ['list_date', 'list_name']


def extract_listings(apidata):
    """
    apidata is a parsed data object (a dict), in the expected api format

    returns a list of dicts:
    """
    listdata = apidata['results']
    listings = []
    for book in listdata['books']:
        d = {'list_date': listdata['bestsellers_date'], 'list_name': listdata['list_name_encoded']}
        d.update({h: book[h] for h in BASIC_BOOK_HEADERS})

        listings.append(d)
    return listings

for listname in listdir(IN_DATA_DIR):
    listings = []
    in_filenames = glob(join(IN_DATA_DIR, listname, '*.json'))
    out_filename = join(OUT_DATA_DIR, '{n}.csv'.format(n=listname))

    if os.path.isfile(out_filename): continue
    print("Reading {num} files from ({list})".format(list=listname, num=len(in_filenames)))
    print("Writing to:", out_filename)
    #is_ok = input("OK?")

    for fn in in_filenames:
        with open(fn, 'r') as rf:
            apidata = json.load(rf)
            try:
                listings.extend(extract_listings(apidata))
            except Exception as err:
                print(err)
                pass

    print("Collected", len(listings), 'listings.')
    with open(out_filename, 'w') as wf:
        c = csv.DictWriter(wf, fieldnames=FULL_HEADERS)
        c.writeheader()
        c.writerows(listings)
