import pickle
import pprint

import dill
"""
with open("gr_series.p", "rb") as f:
    global SERIES; SERIES = pickle.load(f)

with open("gr_books.p", "rb") as f:
    global BOOKS; BOOKS = pickle.load(f)

with open("gr_authors.p", "rb") as f:
    global AUTHORS; AUTHORS = pickle.load(f)

with open("gr_series_author.p", "rb") as f:
    global S_A; S_A = pickle.load(f)

with open("gr_series_book.p", "rb") as f:
    global S_B; S_B = pickle.load(f)
"""

FILES = ["gr_series.p", "gr_books.p", "gr_authors.p", "gr_series_book.p"]


for file in FILES:
    unpickled = {}
    try:
        with open(file, 'rb') as frh:
            unpickled = pickle.load(frh)
            pprint.pprint(unpickled)
        frh.close()
        with open(file, 'wb') as fwh:
            pickle.dump(obj=unpickled, protocol=0, file=fwh)
    except EOFError:
        print(file)
        pprint.pprint(unpickled)
        continue
