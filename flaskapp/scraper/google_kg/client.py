"""Example of Python client calling Knowledge Graph Search API."""
import json
import os
import os.path
import urllib
from os import path
import requests
import pprint

"""
Python client calling Google Knowledge Graph Search API
=======================================================

To specify multiple instances repeat the parameter (e.g. ...?ids=A&ids=B) {ids, languages, types}

@param query: Literal query string for search.
@type query: C{str}

@param ids: Entity id(s) used instead of query string.
@type ids: C{str}

@param languages: The list of language codes (defined in ISO 639) to run the query with, for instance en.
@type languages: C{str}

@param types: Restricts returned entities, e.g. Person (http://schema.org/Person).
@type types: C{str}

@param prefix: Enables prefix match against entities (e.g. Jung will match aliases such as Jung, Jungle, and Jung-ho Kang).
@type prefix: C{boolean}

@param indent: Enables indenting of JSON results.
@type indent: C{boolean}

@param limit: Limits the number of entities to be returned.
@type limit: C{int}

@param key: Developer "browser" key
@type key: C{str}


    Reference:
    ----------
    URL: U{https://developers.google.com/knowledge-graph/}
    Usage Limit: ree quota of up to 100,000 (one hundred thousand) read calls per day per project.
"""
pprint.PrettyPrinter(indent=4)

# GET
# https://kgsearch.googleapis.com/v1/entities:search?
# indent=true
# &languages=en
# &limit=10
# &prefix=true
# &query=Book+Publisher
# &types=Corporation
# &fields=itemListElement
# &key={YOUR_API_KEY}

# https://kgsearch.googleapis.com/v1/entities:search?
# indent=True
# &fields=itemListElement
# &query=Book+Publisher
# &types=Corporation
# &key=AIzaSyBitkWZNZuUvnWmK6vlLX5gphHc8gng72c
# &limit=1000
# &languages=en


#

query = 'Book Publisher'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
api_key = os.environ.get('GKG_KEY')
params = {
    'ids': None,
    'query': query,
    'types': "Corporation",
    'languages': "en",
    'limit': 200,
    'indent': "true",
    'fields': "itemListElement",
    'key': api_key
}

response = requests.get(service_url, params)
print(response.url)
data_dict = response.json()
pprint.pprint(data_dict)
result_list = []
for element in data_dict['itemListElement']:
    d = {}
    result = element['result']
    if result:
        d["score"] = element['resultScore']
        d["kgid"] = result['@id']
        d["name"] = result['name']
        d["desc"] = result.get('description', "")
        d["url"] = result.get('url', "")
        d["image"] = result.get('image', {}).get('contentUrl', "")
        detailedDescription = result.get('detailedDescription', {})
        if detailedDescription:
            d["articleBody"] = detailedDescription['articleBody']
            d["wiki_url"] = detailedDescription['url']
        else:
            d["articleBody"] = ""
            d["wiki_url"] = ""

        result_list.append(d)


pprint.pprint(result_list)

OUTPUT_DIR = path.realpath(path.join(os.path.curdir, 'data'))
OUTFILE = query.replace(" ", "_") + ".json"
OUTFILE_PATH = path.join(OUTPUT_DIR, OUTFILE)

with open(OUTFILE_PATH, 'w') as fp:
    json.dump(result_list,fp)
