""" NYT Books API """

from .base import BaseModel


class ListsNamesResult(BaseModel):
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
    def list_name_encoded(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['list_name_encoded']

    @property
    def oldest_published_date(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['oldest_published_date']

    @property
    def newest_published_date(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['newest_published_date']

    @property
    def updated(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['updated']
