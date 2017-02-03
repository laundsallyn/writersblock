class ISBN:
    def __init__(self, isbn_dict):
        self._isbn_dict = isbn_dict

    @property
    def isbn10(self):
        """
        Gets the list_name of this MList.

        :return: The list_name of this MList.
        :rtype: str
        """
        return self._isbn_dict['isbn10']

    @property
    def isbn13(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._isbn_dict['isbn13']
