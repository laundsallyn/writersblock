class RanksHistory:
    def __init__(self, history_dict):
        self._history_dict = history_dict

    @property
    def primary_isbn10(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._history_dict['primary_isbn10']

    @property
    def primary_isbn13(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._history_dict['primary_isbn13']

    @property
    def rank(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: int
        """
        return self._history_dict['rank']

    @property
    def list_name(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._history_dict['list_name']

    @property
    def display_name(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._history_dict['display_name']

    @property
    def published_date(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._history_dict['published_date']

    @property
    def bestsellers_date(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._history_dict['bestsellers_date']

    @property
    def weeks_on_list(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: int
        """
        return self._history_dict['weeks_on_list']

    @property
    def ranks_last_week(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: null
        """
        return self._history_dict['ranks_last_week']

    @property
    def asterisk(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._history_dict['asterisk']

    @property
    def dagger(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._history_dict['dagger']
