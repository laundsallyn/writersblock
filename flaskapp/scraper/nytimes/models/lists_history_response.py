from .base import BaseModel

""" NYT Books API """


class ListsHistoryResult(BaseModel):
    @property
    def title(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._results_dict['title']

    @property
    def description(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['description']

    @property
    def contributor(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['contributor']

    @property
    def author(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._results_dict['author']

    @property
    def contributor_note(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['contributor_note']

    @property
    def price(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: int
        """
        return self._results_dict['price']

    @property
    def age_group(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['age_group']

    @property
    def publisher(self):
        """
        Gets the updated of this MList.


        :return: The updated of this MList.
        :rtype: str
        """
        return self._results_dict['publisher']

    @property
    def isbns(self):
        """
        Gets the updated of this MList.

        :return: The updated of this MList.
        :rtype: list[ISBN]
        """
        return self._results_dict['isbns']

    @property
    def ranks_history(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: list[RanksHistory]
        """
        return self._results_dict['ranks_history']

    @property
    def lists(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: list[Review]
        """
        return self._results_dict['reviews']
