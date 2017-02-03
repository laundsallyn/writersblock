from .base import BaseModel

""" NYT Books API """


class ListsResult(BaseModel):
    @property
    def list_name(self):
        """
        Gets the list_name of this MList.

        :return: The list_name of this MList.
        :rtype: str
        """
        return self._results_dict['list_name']

    @property
    def display_name(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._results_dict['display_name']

    @property
    def bestsellers_date(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['bestsellers_date']

    @property
    def published_date(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['published_date']

    @property
    def rank(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: int
        """
        return self._results_dict['rank']

    @property
    def rank_last_week(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: int
        """
        return self._results_dict['rank_last_week']

    @property
    def weeks_on_list(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: int
        """
        return self._results_dict['weeks_on_list']

    @property
    def asterisk(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: int
        """
        return self._results_dict['asterisk']

    @property
    def dagger(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: int
        """
        return self._results_dict['dagger']

    @property
    def amazon_product_url(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['amazon_product_url']

    @property
    def isbns(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: list[ISBN]
        """
        return self._results_dict['isbns']

    @property
    def book_details(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: int
        """
        return self._results_dict['book_details']

    @property
    def reviews(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: list[Review]
        """
        return self._results_dict['reviews']
