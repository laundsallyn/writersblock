import os

from ..models.lists_date_list import ListsDateListResult
from ..models.lists_history_response import ListsHistoryResult
from ..models.lists_names_response import ListsNamesResult
from ..models.lists_overview_response import ListsOverviewResult
from ..models.lists_response import ListsResult
from ..models.reviews_response import ReviewsResult
from ...shared.base_client import Client


class NYTimesClient(Client):
    """Initialize the client"""

    def __init__(self):
        _base_url = "http://api.nytimes.com/svc/books/v3"
        _key = os.environ.get('NYT_KEY')

        Client.__init__(self,
                        base_url=_base_url,
                        client_key=_key)

    def get_list_names(self):
        """Get list of lists"""
        resp = self.request(path="/lists/names.json", query_dict=None)
        return ListsNamesResult(resp['results'], self)

    def get_bestseller_history(self,
                               age_group=None,
                               author=None,
                               contributor=None,
                               isbn=None,
                               price=None,
                               publisher=None,
                               title=None):
        """
        Get info about the ranking history of bestseller that satisfy client-provided search parameters

        (For best-seller history requests, the maximum number of results is 20; the offset parameter is not available.)

        """
        resp = self.request(
            path="/lists/best-sellers/history.json",
            query_dict={'age_group': age_group,
                        'author': author,
                        'contributor': contributor,
                        'isbn': isbn,
                        'price': price,
                        'publisher': publisher,
                        'title': title
                        }
        )
        return ListsHistoryResult(resp['results'], self)

    def search_bestsellers(self,
                           list_name=None,
                           weeks_on_list=None,
                           date=None,
                           isbn=None,
                           rank=None,
                           rank_last_week=None,
                           offset=None):
        """
        search best-seller list data, using the following URI structure:
            http://api.nytimes.com/svc/books/{version}/lists.json
                ?{search-param1=value1}&[...]
                &[optional-param1=value1]&[...]
                &api-key={your-API-key}

        The service returns 20 results at a time. Use the offset parameter to page through the results.
        """
        resp = self.request(
                path="/lists/best-sellers/history.json",
                query_dict={
                    'list': list_name,
                    'weeks_on_list': weeks_on_list,
                    'date': date,
                    'isbn': isbn,
                    'rank': rank,
                    'rank_last_week': rank_last_week,
                    'offset': offset
                }
        )
        return ListsResult(resp['results'], self)

    def get_list_overviews(self, published_date):
        """
        Get info about an author

        :param published_date: The best-seller list publication date. YYYY-MM-DD
        :type published_date: str

        If you do not include a published_date, the current week's best-sellers lists will be returned.

        """
        resp = self.request(
                path="/lists/overview.json",
                query_dict={'published_date': published_date}
        )
        return ListsOverviewResult(resp['results'], self)

    def get_bestseller_list(self,
                            date=None,
                            list_name=None,
                            *,
                            isbn=None,
                            weeks_on_list=None,
                            rank=None,
                            rank_last_week=None,
                            offset=None):
        """
        GET a particular Times best-seller list

           uses the following URI structure:
                http://api.nytimes.com/svc/books/{version}/lists/
                    [date/]{list-name}.json
                    ?[optional-param1=value1]&[...]
                    &api-key={your-API-key}

        """
        resp = self.request(
                path="/lists/{date}/{list}.json".format(date=date, list=list_name),
                query_dict={
                    'isbn': isbn,
                    'weeks_on_list': weeks_on_list,
                    'rank': rank,
                    'rank_last_week': rank_last_week,
                    'offset': offset
                }
        )
        return ListsDateListResult(resp['results'], self)

    def get_reviews(self, isbn=None, title=None, author=None):
        """
        Get reviews on a bestseller

        Searching by ISBN is the recommended method.
        You can enter 10- or 13-digit ISBNs.

        You’ll need to enter the full title of the book.
        You’ll need to enter the author’s first and last name,

        Spaces will be converted into the characters %20.

        """
        resp = self.request(
                path="/lists/names.json",
                query_dict={'isbn': isbn, 'title': title, 'author': author}
        )
        return ReviewsResult(resp['results'], self)
