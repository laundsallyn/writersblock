class RankBook:
    def __init__(self, book_dict):
        self._book_dict = book_dict

    @property
    def rank(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: int
        """
        return self._book_dict['rank']

    @property
    def rank_last_week(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: int
        """
        return self._book_dict['rank_last_week']

    @property
    def weeks_on_list(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: int
        """
        return self._book_dict['weeks_on_list']

    @property
    def asterisk(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: int
        """
        return self._book_dict['asterisk']

    @property
    def dagger(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: int
        """
        return self._book_dict['dagger']

    @property
    def primary_isbn10(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['primary_isbn10']

    @property
    def primary_isbn13(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['primary_isbn13']

    @property
    def publisher(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['publisher']

    @property
    def description(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._book_dict['description']

    @property
    def price(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: int
        """
        return self._book_dict['price']

    @property
    def title(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['title']

    @property
    def author(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._book_dict['author']

    @property
    def contributor(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['contributor']

    @property
    def contributor_note(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['contributor_note']

    @property
    def book_image(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['book_image']

    @property
    def amazon_product_url(self):
        """
        Gets the newest_published_date of this ResultListsNames.

        :return: The newest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['amazon_product_url']

    @property
    def age_group(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: str
        """
        return self._book_dict['age_group']

    @property
    def book_review_link(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._book_dict['book_review_link']

    @property
    def first_chapter_link(self):
        """
        Gets the oldest_published_date of this ResultListsNames.

        :return: The oldest_published_date of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['first_chapter_link']

    @property
    def sunday_review_link(self):
        """
        Gets the display_name of this MList.

        :return: The display_name of this MList.
        :rtype: str
        """
        return self._book_dict['sunday_review_link']

    @property
    def article_chapter_link(self):
        """
        Gets the list_name_encoded of this ResultListsNames.

        :return: The list_name_encoded of this ResultListsNames.
        :rtype: str
        """
        return self._book_dict['article_chapter_link']

    @property
    def isbns(self):
        """
        Gets the list_name of this MList.


        :return: The list_name of this MList.
        :rtype: list[ISBN]
        """
        return self._book_dict['isbns']
