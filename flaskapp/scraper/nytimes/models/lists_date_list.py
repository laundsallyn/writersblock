from .base import BaseModel

""" NYT Books API """


class ListsDateListResult(BaseModel):
    @property
    def list_name(self):
        """
        Gets the list_name of this MList.

        :return: The list_name of this MList.
        :rtype: str
        """
        return self._results_dict['list_name']

    @property
    def bestsellers_date(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
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
    def display_name(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._results_dict['display_name']

    @property
    def normal_list_ends_at(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['normal_list_ends_at']

    @property
    def updated(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['updated']

    @property
    def books(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: list[RankBook]
        """
        return self._results_dict['books']

    @property
    def corrections(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: list
        """
        return self._results_dict['corrections']
