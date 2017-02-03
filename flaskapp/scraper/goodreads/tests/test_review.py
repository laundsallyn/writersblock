from ..fetch.client import GoodreadsClient
from ..models.review import GoodreadsReview
from nose.tools import eq_, ok_


class TestReview:
    @classmethod
    def setup_class(cls):
        cls.client = GoodreadsClient()

    def test_recent_reviews(self):
        reviews = self.client.recent_reviews()
        ok_(all(isinstance(r, GoodreadsReview) for r in reviews))

    def test_review(self):
        review = self.client.review('2')
        eq_(review.gid, '2')
        pass
