"""Client test functions"""

from ..fetch.client import GoodreadsClient
from ..models.book import GoodreadsBook
import unittest

class TestClient():
    @classmethod
    def setup_class(cls):
        cls.client = GoodreadsClient()

    def test_client_setup(self):
        assert self.client.base_url=="https://www.goodreads.com/"
        assert self.client.response_root =='GoodreadsResponse'

    def test_author_by_id(self):
        author_id = '8566992'
        author = self.client.author(author_id)
        assert author.gid == author_id

    def test_author_by_name(self):
        author_name = 'Richard Dawkins'
        author = self.client.find_author(author_name)
        assert author.name == author_name

    def test_book_by_id(self):
        book_id = '11870085'
        book = self.client.book(book_id)
        assert book.gid == book_id

    def test_search_books(self):
        books = self.client.search_books("The selfish gene")
        assert len(books) > 0
        assert all(isinstance(book, GoodreadsBook) for book in books)
