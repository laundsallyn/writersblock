import pprint

import requests
import sys
import xmltodict

API_ENDPOINT = 'https://www.goodreads.com/book'


def fetch_book_ids(api_key, isbns):
    """
    arguments:
        `api_key` is Goodreads API key
        `isbns` is either a sequence of isbns string; or a comma-delimited string

    returns:
        A requests.Response object...
            let the calling user decide what to extract from it
    """
    if type(isbns) is str:
        isbntxt = isbns
    else:
        isbntxt = ','.join(str(i) for i in isbns)
    url = API_ENDPOINT + '/isbn_to_id'
    params = {'key': api_key, 'isbn': isbntxt}
    return requests.get(url, params)


def fetch_work_ids(api_key, bids):
    """
    arguments:
        `api_key` is Goodreads API key
        `isbns` is either a sequence of isbns string; or a comma-delimited string

    returns:
        A requests.Response object...
            let the calling user decide what to extract from it
    """
    if type(bids) is str:
        bidtxt = bids
    else:
        bidtxt = ','.join(str(i) for i in bids)
    url = API_ENDPOINT + '/id_to_work_id'
    params = {'key': api_key, 'id': bidtxt}
    resp = requests.get(url, params)

    data_dict = xmltodict.parse(resp.content)
    return data_dict["GoodreadsResponse"]["work-ids"]["item"]


def fetch_show_book(api_key, id):
    """
    arguments:
        `api_key` is Goodreads API key
        `id` is Goodreads Book ID

    returns:
        A requests.Response object...
            let the calling user decide what to extract from it
    """
    mypath = '/show.xml'
    myparams = {'key': api_key, 'id': id}
    myurl = API_ENDPOINT + mypath
    return requests.get(myurl, myparams)
