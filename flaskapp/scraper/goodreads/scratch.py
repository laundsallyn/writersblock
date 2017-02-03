import csv
import json
import os.path
import pickle
import pprint
import time

import requests
import xmltodict

DATA_DIR = os.path.join(os.path.curdir, 'data')
INDATA = os.path.join(DATA_DIR, 'ISBN2GRbid.csv')
OUTDATA = os.path.join(DATA_DIR, 'WID2WSD.csv')
OUTDIR = os.path.join(DATA_DIR, 'series')
API_ENDPOINT = 'https://www.goodreads.com/work/'


def gather_unique_wids():

    wids = []
    with open(INDATA, 'rt') as csvfile:
        isbn_gid = csv.reader(csvfile, delimiter=',')

        for bid, wid in isbn_gid:
            if wid:
                wids.append(wid)

    uniq_wids = list(set(wids))
    return uniq_wids


def wid_series(api_key, id, session):
    """
    arguments:
        `api_key` is Goodreads API key
        `id` is Goodreads Book ID

    returns:
        A requests.Response object...
            let the calling user decide what to extract from it
    """
    mypath = '/series'
    myparams = {'key': api_key, 'format': "xml"}
    myurl = API_ENDPOINT + str(id) + mypath
    print(myurl)
    resp = s.get(myurl, params=myparams)
    if resp.status_code != 200:
        return None
    data_dict = xmltodict.parse(resp.content)

    pprint.pprint(data_dict)
    return data_dict["GoodreadsResponse"]["series_works"]


if __name__ == '__main__':
    apikey = os.environ.get("GR_KEY")
"""
    wids = gather_unique_wids()
    s = requests.Session()
    WID2SID = []
    with open(OUTDATA, 'wt') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for w in wids:
            resp = wid_series(api_key=apikey, id=w, session=s)
            if resp:

                for k, v in resp.items():
                    print(k, v)
                    if type(v) == list:
                        for e in v:
                            print(e)
                            sid = e['series']['id']
                            WID2SID.append({w: sid})
                            writer.writerow([w, sid])
                            print(w, sid)
                    else:
                        sid = v['series']['id']
                        WID2SID.append({w: sid})
                        writer.writerow([w, sid])
                        print(w, sid)

    with open('WID2SID.p', 'w') as f:
        pickle.dump(WID2SID, f)
"""

ses = requests.session()
resp = {}

id_list = gather_unique_wids()

for i in id_list:
    #urla = "https://www.goodreads.com/series/list/{idx}.xml?key=UEjJ8JPVjwhYdPBBzZw".format(idx=str(i)) #2100
    #urls = "https://www.goodreads.com/series/show/{idx}.xml?key=UEjJ8JPVjwhYdPBBzZw".format(idx=str(i))
    url = "https://www.goodreads.com/series/work/{idx}?format=xml&key=UEjJ8JPVjwhYdPBBzZw".format(idx=str(i))
    print(url)
    resp = ses.get(url)
    if resp.status_code != 200: continue
    if resp.content:
        data_dict = xmltodict.parse(resp.content)

        fn = os.path.join(OUTDIR, "sid{sid}.json".format(sid=str(i)))
        json.dump(data_dict, open(fn, 'w'))






