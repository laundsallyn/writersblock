from ..fetch.client import GoodreadsClient
from ..models.author import GoodreadsAuthor
from ..models.book import GoodreadsBook


class TestAuthor:
    @classmethod
    def setup_class(cls):
        client = GoodreadsClient()
        cls.author = client.author('64941')

    def test_get_author(self):
        assert isinstance(self.author, GoodreadsAuthor)
        assert self.author.gid == '64941'

    def test_author_name(self):
        assert self.author.name == 'Donald Ervin Knuth'

    def test_author_books(self):
        books = self.author.books
        assert all(isinstance(book, GoodreadsBook) for book in books)
        assert (books[-1].title == 'Literate Programming')
