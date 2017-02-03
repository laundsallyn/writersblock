#!/usr/bin/env python
from unittest import main, TestCase

from models import Base, Author, Book, Series, Publisher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MyTest(TestCase):
    # engine = create_engine('sqlite:////tmp/test.db')
    engine = create_engine('sqlite://')
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def setUpClass(cls):
        """
        # Creates a new database for the unit test to use
        """
        cls.engine.execute('DROP TABLE IF EXISTS authors;')
        cls.engine.execute('DROP TABLE IF EXISTS books;')
        cls.engine.execute('DROP TABLE IF EXISTS series;')
        cls.engine.execute('DROP TABLE IF EXISTS publishers;')
        cls.engine.execute('DROP TABLE IF EXISTS assoc_author_book;')
        cls.engine.execute('DROP TABLE IF EXISTS assoc_author_series;')

        Base.metadata.create_all(cls.engine)
        dostoyevsky = Author(
                name="Fyodor Dostoyevsky",
                date_of_birth="1821-11-11",
                nationality="Russian"
                # homepage_URL = null
        )
        keats = Author(
                name="John Keats",
                date_of_birth="1821-2-23",
                nationality="British",
                occupation="Poet"
                # homepage_URL = null
        )
        tolstoy = Author(
                name="Leo Tolstoy",
                date_of_birth="1828-9-9",
                nationality="Russian"
                # homepage_URL = null
        )
        murakami = Author(
                name="Haruki Murakami",
                date_of_birth="1949-1-12",
                nationality="Japanese",
                homepage_URL="www.harukimurakami.com"
        )
        # adding publishers
        penguin = Publisher(
                name="Penguin",
                founder="Allen Lane",
                year_founded="1935",
                country="United Kingdom",
                status="Active")

        vintage = Publisher(
                name="Vintage",
                founder="Alfred A. Knopf, Sr.",
                year_founded="1954",
                country="United States",
                status="Active")

        knopf = Publisher(
                name="Knopf",
                founder="Alfred A. Knopf, Sr.",
                country="United States",
                status="Active")

        oxford = Publisher(
                name="Oxford University Press",
                country="United Kingdom")

        oneq84 = Series(
                title="1Q84",
                genre="Magical Realism",
                num_books=3,
                status=1
        )
        oneq84.written_by = [murakami]

        bis = Book(
                title="1Q84, #1-3",
                isbn="0307593312"
        )

        bis.written_by = [murakami]
        bis.publisher = knopf
        bis.in_series = oneq84

        war_and_peace = Book(
                title="War and Peace",
                isbn="0192833987"
        )

        notes_from_underground = Book(
                title="Notes from Underground",
                isbn="067973452X"
        )

        crime_and_punishment = Book(
                title="Crime and Punishment",
                isbn="0143058142"
        )
        tolstoy.wrotes = [war_and_peace]
        dostoyevsky.wrotes = [notes_from_underground]
        oxford.published_book = [war_and_peace]
        vintage.published_book = [notes_from_underground]
        crime_and_punishment.written_by = [dostoyevsky]
        crime_and_punishment.publisher = penguin  # books to publishers: many to one

        tolkien = Author(
                name="J. R. R. Tolkien",
                date_of_birth="1892-1-3",
                nationality="British",
                occupation="Philologist"
        )

        houghton_mifflin_harcourt = Publisher(
                name="Houghton Mifflin Harcourt",
                founder="Henry Oscar Houghton",
                country="United States",
                status="Active"
        )

        del_rey = Publisher(
                name="Del Rey",
                founder="Lester del Rey",
                status="Active")

        hobbit = Book(
                title="The Hobbit",
                isbn="0618260307"
        )
        hobbit.written_by = [tolkien]
        hobbit.publisher = houghton_mifflin_harcourt

        rings = Series(
                title="The Lord of the Rings",
                genre="Epic",
                num_books=3,
                status=1)
        ring1 = Book(
                title="The Fellowship of the Ring",
                isbn="0618346252")
        ring1.written_by = [tolkien]
        ring1.publisher = houghton_mifflin_harcourt
        ring1.in_series = rings

        ring2 = Book(
                title="The Two Towers",
                isbn="0618346260"
        )
        ring2.written_by = [tolkien]
        ring2.publisher = houghton_mifflin_harcourt
        ring2.in_series = rings

        ring3 = Book(
                title="The Return of the King",
                isbn="0345339738"
        )
        ring3.written_by = [tolkien]
        ring3.publisher = del_rey
        ring3.in_series = rings
        # add The Lord of the Rings related
        cls.session.add(houghton_mifflin_harcourt)
        cls.session.add(del_rey)
        cls.session.add(ring2)
        cls.session.add(ring1)
        cls.session.add(ring3)
        cls.session.add(hobbit)

        # add publishers
        cls.session.add(knopf)
        cls.session.add(penguin)
        cls.session.add(vintage)
        cls.session.add(oxford)
        # add books
        cls.session.add(crime_and_punishment)
        # add authors
        cls.session.add(dostoyevsky)
        cls.session.add(keats)
        cls.session.add(tolstoy)
        cls.session.add(murakami)
        # add series
        cls.session.add(oneq84)

        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        """
        Ensures that the database is emptied for next unit test
        """
        Base.metadata.drop_all(cls.engine)

    def test_series_size(self):
        self.assertEqual(len(self.session.query(Series).all()), 2)

    def test_publisher_size(self):
        self.assertEqual(len(self.session.query(Publisher).all()), 6)

    def test_author_query_1(self):
        book = self.session.query(Author).filter_by(
                name='Fyodor Dostoyevsky').first()
        self.assertEqual(book.nationality, "Russian")
        self.assertEqual(book.occupation, "Writer")
        # self.assertEqual(book.id, 1)

    def test_author_query_3(self):
        book = self.session.query(Author).filter_by(occupation='Poet').first()
        self.assertEqual(book.name, "John Keats")
        self.assertEqual(book.occupation, "Poet")

    def test_author_query_2(self):
        book = self.session.query(Author).filter_by(name='Leo Tolstoy').first()
        self.assertEqual(book.nationality, "Russian")
        self.assertEqual(book.occupation, "Writer")

    def test_book_query_1(self):
        book = self.session.query(Book).filter_by(title='War and Peace').first()
        self.assertEqual(book.title, "War and Peace")
        self.assertEqual(book.written_by[0].name, "Leo Tolstoy")
        self.assertEqual(book.publisher.name, "Oxford University Press")
        self.assertEqual(book.isbn, "0192833987")

    def test_add_book_1(self):
        written_by = "Haruki Murakami"
        kafka_on_the_shore = Book(
                title="Kafka on the Shore",
                isbn="1400079276"
        )
        author = self.session.query(
                Author).filter_by(name=written_by).first()
        author.wrotes = [kafka_on_the_shore]
        self.session.commit()
        # test
        test = self.session.query(Author).filter_by(name=written_by).first()
        book = test.wrotes[0]
        self.assertEqual(book.title, "Kafka on the Shore")
        self.assertEqual(book.written_by[0].name, "Haruki Murakami")

    def test_add_book_2(self):
        written_by = "Haruki Murakami"
        publisher = "Knopf"
        after_dark = Book(
                title="After Dark",
                isbn="0307265838"
        )
        author = self.session.query(
                Author).filter_by(name=written_by).first()
        author.wrotes = [after_dark]
        pubook = self.session.query(Publisher).filter_by(name=publisher).first()
        pubook.published_book = [after_dark]
        self.session.commit()
        # test
        test = self.session.query(Author).filter_by(name=written_by).first()
        book = test.wrotes[0]
        self.assertEqual(book.title, "After Dark")
        self.assertEqual(book.written_by[0].name, "Haruki Murakami")

    def test_add_book_3(self):
        written_by = "Haruki Murakami"
        publisher = "Knopf"
        tsukuru = Book(
                title="Colorless Tsukuru Tazaki and His Years of Pilgrimage",
                isbn="0385352107"
        )
        author = self.session.query(
                Author).filter_by(name=written_by).first()
        pubook = self.session.query(Publisher).filter_by(name=publisher).first()
        author.wrotes = [tsukuru]
        pubook.published_book = [tsukuru]
        self.session.commit()
        # test
        test = self.session.query(Author).filter_by(name=written_by).first()
        book = test.wrotes[0]
        self.assertEqual(
                book.title, "Colorless Tsukuru Tazaki and His Years of Pilgrimage")
        self.assertEqual(book.written_by[0].name, "Haruki Murakami")

    def test_wrotes_1(self):
        author = self.session.query(Author).filter_by(
                name='Fyodor Dostoyevsky').first()
        self.assertEqual(len(author.wrotes.all()), 2)

    def test_book_query_2(self):
        book = self.session.query(Book).filter_by(
                title='Notes from Underground').first()
        self.assertEqual(book.title, "Notes from Underground")
        self.assertEqual(book.written_by[0].name, "Fyodor Dostoyevsky")
        self.assertEqual(book.publisher.name, "Vintage")
        self.assertEqual(book.isbn, "067973452X")

    def test_book_query_3(self):
        book = self.session.query(Book).filter_by(
                title='Crime and Punishment').first()
        self.assertEqual(book.title, "Crime and Punishment")
        self.assertEqual(book.written_by[0].name, "Fyodor Dostoyevsky")
        self.assertEqual(book.publisher.name, "Penguin")

    def test_series_query_1(self):
        book = self.session.query(Series).filter_by(title='1Q84').first()
        self.assertEqual(book.num_books, 3)
        self.assertEqual(book.status, 1)

    def test_series_query_2(self):
        book = self.session.query(Series).filter_by(title='1Q84').first()
        self.assertEqual(book.books[0].title, "1Q84, #1-3")

    def test_lord_of_the_rings_1(self):
        book = self.session.query(Series).filter_by(
                title='The Lord of the Rings').first()
        self.assertEqual(book.num_books, 3)
        self.assertEqual(book.status, 1)

    def test_num_books_in_rings(self):
        series = self.session.query(Series).filter_by(
                title='The Lord of the Rings').first()
        self.assertEqual(len(series.books.all()), 3)

    def test_query_book_in_rings(self):
        series = self.session.query(Series).filter_by(
                title='The Lord of the Rings').first()
        book = series.books.filter_by(title='The Two Towers').first()
        self.assertEqual(book.title, 'The Two Towers')
        self.assertEqual(book.written_by[0].name, "J. R. R. Tolkien")
        self.assertEqual(book.publisher.name, "Houghton Mifflin Harcourt")


if __name__ == '__main__':
    try:
        main()
    except:
        pass
