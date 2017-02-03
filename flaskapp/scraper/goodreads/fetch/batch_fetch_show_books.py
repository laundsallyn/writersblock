# Assume that nytimes/fetched/bestseller-lists/**/*.json
# contains JSON files

import json
from glob import glob
from os.path import join

INPUT_DATADIR = join('data', 'nytimes', 'fetch', 'bestseller-lists')
input_filenames = glob(join(INPUT_DATADIR, '**', '*.json'))

isbn_numbers = []
print(INPUT_DATADIR)
for fname in input_filenames:
    with open(fname, 'r') as rf:
        booksdata = json.load(rf)['results']['books']
    isbn_numbers.extend([b['primary_isbn13'] for b in booksdata])

print('Total isbn numbers', len(isbn_numbers))
uniq_isbn_numbers = set(isbn_numbers)
print('Unique isbn numbers', len(uniq_isbn_numbers))
