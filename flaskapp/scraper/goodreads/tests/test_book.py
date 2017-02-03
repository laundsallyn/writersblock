from ..fetch.client import GoodreadsClient
from ..models.book import GoodreadsBook


class TestBook:
    @classmethod
    def setup_class(cls):
        client = GoodreadsClient()
        cls.book = client.book('11870085')

    def test_get_book(self):
        assert isinstance(self.book, GoodreadsBook)
        assert self.book.gid == '11870085'
