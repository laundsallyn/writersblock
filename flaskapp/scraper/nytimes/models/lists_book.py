class OverviewBook:
    def __init__(self, book_dict):
        self._book_dict = book_dict

    @property
    def title(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['title']

    @property
    def description(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._book_dict['description']

    @property
    def contributor(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['contributor']

    @property
    def author(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._book_dict['author']

    @property
    def contributor_note(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['contributor_note']

    @property
    def price(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: int
        """
        return self._book_dict['price']

    @property
    def age_group(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._book_dict['age_group']

    @property
    def publisher(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['publisher']

    @property
    def primary_isbn13(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['primary_isbn13']

    @property
    def primary_isbn10(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['primary_isbn10']
