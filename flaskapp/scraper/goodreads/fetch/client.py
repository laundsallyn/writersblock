import collections
import os

from ..models.book import GoodreadsBook
from ..models.series import GoodreadsSeries
from ..models.author import GoodreadsAuthor
from ..models.comment import GoodreadsComment
from ..models.review import GoodreadsReview
from scraper.shared.clients import BaseClient
from scraper.shared.exceptions import ClientException


class GoodreadsClient(BaseClient):
    """ Initialize the client through parents Meta Class"""
    class Meta:
        name = "GoodreadsClient"
        base_url = "https://www.goodreads.com/"
        response_root = 'GoodreadsResponse'
        client_key = os.environ.get("GR_KEY")

    def author(self, author_id):
        """Get info about an author"""
        resp = self.request("author/show/{}".format(author_id), {})
        return GoodreadsAuthor(resp['author'], self)

    def find_author(self, author_name):
        """Find an author by name"""
        resp = self.request("api/author_url/{!s}".format(author_name), {})
        return self.author(resp['author']['@id']) if 'author' in resp else None

    def book(self, book_id=None, isbn=None):
        """Get info about a book"""
        if book_id:
            resp = self.request("book/show/", {'id': book_id})
            return GoodreadsBook(resp['book'], self)
        elif isbn:
            resp = self.request("book/isbn/", {'isbn': isbn})
            return GoodreadsBook(resp['book'], self)
        else:
            raise ClientException("book id or isbn required")

    def series(self, series_id=None):
        """Get info about a book"""
        if series_id:
            resp = self.request("series/{}".format(series_id), {})
            return GoodreadsSeries(resp['series'], self)
        else:
            raise ClientException("series_id required")

    def search_books(self, q, page=1, search_field='all'):
        """Get the most popular books for the given query. This will search all
        books in the title/author/ISBN fields and show matches, sorted by
        popularity on Goodreads.

        :param q: query text
        :param page: which page to return (default 1)
        :param search_field: field to search, one of 'title', 'author' or
        'genre' (default is 'all')
        """
        resp = self.request("search/index.xml",
                            {'q': q, 'page': page, 'search[field]': search_field})
        works = resp['search']['results']['work']
        # If there's only one work returned, put it in a list.
        if type(works) == collections.OrderedDict:
            works = [works]
        return [self.book(work["best_book"]['id']['#text']) for work in works]

    def book_review_stats(self, isbns):
        """Get review statistics for books given a list of ISBNs"""
        resp = self.request("book/review_counts.json",
                            {'isbns': ','.join(isbns)},
                            req_format='json')
        return resp['books']

    """ comment_type should be one of: """
    """comment_type_enum = enum.Enum('author_blog_post', 'blog', 'book_news_post', 'chapter', 'comment', 'community_answer',
                                  'event_response', 'fanship', 'friend', 'giveaway', 'giveaway_request', 'group_user',
                                  'interview', 'librarian_note', 'link_collection', 'list', 'owned_book', 'photo', 'poll',
                                  'poll_vote', 'queued_item', 'question', 'question_user_stat', 'quiz', 'quiz_score',
                                  'rating', 'read_status', 'recommendation', 'recommendation_request', 'review', 'topic',
                                  'user', 'user_challenge', 'user_following', 'user_list_challenge', 'user_list_vote',
                                  'user_quote', 'user_status', 'video')"""

    def list_comments(self, comment_type, resource_id, page=1):
        """List comments on a subject"""
        resp = self.request(u"{0:s}/{1:s}/comments".format(comment_type, resource_id), {'format': 'xml'})
        return [GoodreadsComment(comment_dict)
                for comment_dict in resp['comments']['comment']]

    def recent_reviews(self):
        """Get the recent reviews from all members"""
        resp = self.request("/review/recent_reviews.xml", {})
        return [GoodreadsReview(r) for r in resp['reviews']['review']]

    def review(self, review_id):
        """Get a review"""
        resp = self.request("/review/show.xml", {'id': review_id})
        return GoodreadsReview(resp['review'])
