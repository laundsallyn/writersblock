""" NYT Books API """

from .base import BaseModel


class ListsOverviewResult(BaseModel):
    @property
    def bestsellers_date(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._results_dict['bestsellers_date']

    @property
    def lists(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: list[overview_list]
        """
        return self._results_dict['lists']

    @property
    def byline(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['byline']

    @property
    def book_title(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['book_title']

    @property
    def book_author(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['book_author']

    @property
    def summary(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['summary']

    @property
    def isbn13(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: list[str]
        """
        return self._results_dict['isbn13']
