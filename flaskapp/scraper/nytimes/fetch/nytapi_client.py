import csv
import json
import re

import scraper.shared.clients as clients
import scraper.shared.resources as resources


class NamesResource(resources.BaseResource):
    class Meta:
        name = 'Names'
        resource_name = 'names'
        identifier = 'list_name_encoded'
        attributes = (
            'list_name_encoded',
            'oldest_published_date',
            'newest_published_date',
            'updated',
        )
        pagination_key = 'results'


class ListResource(resources.BaseResource):
    class Meta:
        name = 'Lists'
        resource_name = 'lists'
        identifier = 'list_name_encoded'
        attributes = (
            'list_name_encoded',
            'published_date',
            'books',
        )
        pagination_key = 'results'


class RankHistoryResource(resources.BaseResource):
    class Meta:
        name = 'History'
        resource_name = 'history'
        identifier = 'title'
        attributes = (
            'title',
            'description',
            'author',
            'price',
            'age_group',
            'publisher',
            'isbns',
            'reviews',
        )
        pagination_key = 'results'

    @classmethod
    def get_url(cls, url, uid, **kwargs):
        """
        Our customised URL.
        """
        print(url)
        return 'http://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json'


class NYTClient(clients.BaseClient):
    class Meta:
        name = 'NYT Books API'
        base_url = 'http://api.nytimes.com/svc/books/v3/lists'
        resources = (NamesResource, ListResource, RankHistoryResource)
        client_key = "NYT_KEY"


nytc = NYTClient()
results_list = nytc.get_names()

print(json.dumps(results_list, default=lambda o: o.__dict__))

history_list = []
results_list = nytc.get_history()
for r in results_list:
    reviews = r.reviews[0]

    if r.isbns and r.publisher:
        d = dict(
            title=r.title,
            author=re.split(" (&|and) ", r.author),
            isbn=r.isbns[0].get("isbn13", ""),
            description=r.description,
            publisher=r.publisher,
            price=r.price,
            age_group=r.age_group,
            review=reviews.get("sunday_review_link", ""),
        )
        history_list.append(d)
    else:
        print(json.dumps(r, default=lambda o: o.__dict__))


keys = history_list[0].keys()
print(keys)
with open("history_list.csv", 'w') as wf:
    c = csv.DictWriter(wf, keys)
    c.writeheader()
    c.writerows(history_list)

print(json.dumps(history_list, default=lambda o: o.__dict__))
