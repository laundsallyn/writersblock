class Review:
    def __init__(self, review_dict):
        self._review_dict = review_dict

    @property
    def book_review_link(self):
        """
        Gets the list_name of this MList.

        :return: The list_name of this MList.
        :rtype: str
        """
        return self._review_dict['book_review_link']

    @property
    def first_chapter_link(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._review_dict['first_chapter_link']

    @property
    def sunday_review_link(self):
        """
        Gets the list_name of this MList.

        :return: The list_name of this MList.
        :rtype: str
        """
        return self._review_dict['sunday_review_link']

    @property
    def article_chapter_link(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._review_dict['article_chapter_link']
