class OverviewList:
    def __init__(self, list_dict):
        self._list_dict = list_dict

    @property
    def list_id(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._list_dict['list_id']

    @property
    def list_name(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._list_dict['list_name']

    @property
    def display_name(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._list_dict['display_name']

    @property
    def updated(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._list_dict['updated']

    @property
    def books(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: list[OverviewBook]
        """
        return self._list_dict['books']
