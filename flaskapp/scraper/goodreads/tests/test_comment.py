from ..fetch.client import GoodreadsClient
from ..models.comment import GoodreadsComment
from nose.tools import ok_


class TestComment:
    @classmethod
    def setup_class(cls):
        client = GoodreadsClient()
        cls.comments = client.list_comments('user', '1')

    def test_list_comments(self):
        ok_(all(isinstance(c, GoodreadsComment) for c in self.comments))
