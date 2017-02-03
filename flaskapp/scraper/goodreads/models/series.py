"""Goodreads series class"""


class GoodreadsSeries(object):
    def __init__(self, series_dict: dict, client):
        self._series_dict = series_dict
        self._client = client

    def __repr__(self):
        return self.series_title

    @property
    def sid(self):
        """Goodreads id of the book"""
        return self._series_dict['id']

    @property
    def series_title(self):
        """Information on the original work"""
        return self._series_dict['title']

    @property
    def series_desc(self):
        """Return series of the book"""
        return self._series_dict['description']

    @property
    def note(self):
        """Return series of the book"""
        return self._series_dict['note']

    @property
    def series_works_cnt(self):
        """Title of the book"""
        return self._series_dict['series_works_count']

    @property
    def primary_works_cnt(self):
        """Title of the book"""
        return self._series_dict['primary_work_count']

    @property
    def is_numbered(self):
        """Is this a numbered series?"""
        return self._series_dict['numbered']

    @property
    def series_works(self):
        """Return the works of the series"""
        return [
            self.Work(series_work_dict)
            for series_work_dict
            in self._series_dict['series_works']
            ]

    class Work:
        def __init__(self, series_dict):
            self._series_work__dict = series_dict

        @property
        def series_work_id(self):
            """Goodreads id of the book"""
            return self._series_work__dict['id']

        @property
        def series_position(self):
            """Information on the original work"""
            return self._series_work__dict['user_position']

        @property
        def work(self):
            """Return series of the book"""
            return self._series_work__dict['work']

        @property
        def work_id(self):
            """Return series of the book"""
            return self._series_work__dict['work']['id']

        @property
        def pub_year(self):
            """Title of the book"""
            return self._series_work__dict['work']['original_publication_year']

        @property
        def orig_title(self):
            """Title of the book"""
            return self._series_work__dict['work']['original_title']

        @property
        def best_book(self):
            """Title of the book"""
            return self._series_work__dict['work']['best_book']

        @property
        def bb_id(self):
            """Title of the book"""
            return self._series_work__dict['work']['best_book']['id']

        @property
        def title(self):
            """Title of the book"""
            return self._series_work__dict['work']['best_book']['title']

        @property
        def title(self):
            """Title of the book"""
            return self._series_work__dict['work']['best_book']['title']

        @property
        def author(self):
            """Title of the book"""
            return self._series_work__dict['work']['best_book']['author']

        @property
        def img(self):
            """Title of the book"""
            return self._series_work__dict['work']['best_book']['image_url']
