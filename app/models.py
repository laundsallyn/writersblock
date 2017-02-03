#!/usr/bin/env/python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Table, ForeignKey
from datetime import date
from sqlalchemy.orm import relationship

Base = declarative_base()
"""assoc_author_book is an intermidate tables
that establishes the many to many relationship
between authors and books"""
assoc_author_book = Table('assoc_ab', Base.metadata,
                          Column(
                              'author_id', Integer, ForeignKey('authors.id')),
                          Column('book_id', Integer, ForeignKey('books.id'))
                          )

"""assoc_author_book is an intermidate tables
that establishes the many to many relationship
between authors and series"""

assoc_author_series = Table('assoc_as', Base.metadata,
                            Column(
                                'author_id', Integer, ForeignKey('authors.id')),
                            Column(
                            'series_id', Integer, ForeignKey('series.id'))
                            )



"""Series stores information about a series
it contains id, title, genre, number of books in that series, status, author and publisher
"""


class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    num_books = Column(Integer)
    status = Column(Integer)  # 0 for active, 1 for finished
    author_id = Column(Integer, ForeignKey('authors.id'))

    books = relationship("Book", back_populates='in_series',lazy = 'dynamic')
    
    written_by = relationship(
        "Author",
        secondary=assoc_author_series,
        back_populates="wrotes_series",lazy='dynamic')
    
    # def __init__(self, title, author, publisher, num_books, genre = "Novel", status = None):
    #     self.title = title
    #     self.genre = genre
    #     self.written_by = author
    #     self.num_books = num_books
    #     self.published_by = publisher
    #     self.status = status
    def get_basic_info(self):
        info = (self.id, self.title. self.genre, self.num_books, self.status)

        return info
""" Book relation stores specific information about a book.
it has attributes id, title, isbn, author, series, publisher
"""

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    isbn = Column(String, unique = True)
    image_link = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    series_id = Column(Integer, ForeignKey('series.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))

    in_series = relationship("Series", back_populates='books')
    publisher = relationship("Publisher", back_populates='published_book')
    written_by = relationship(
        "Author",
        secondary=assoc_author_book,
        back_populates="wrotes",lazy='dynamic')


    # def __init__(self, title, author, isbn, publisher=None, in_series=None):
    #     self.title = title
    #     self.written_by = author
    #     self.isbn = isbn
    #     self.publisher = publisher
    #     self.in_series = in_series



"""Publisher stores information abotu a publisher
it has attributes id, name, founder, year_founded, country and status.
publisher has relationship to series and books"""


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    founder = Column(String)
    year_founded = Column(String)
    country = Column(String)
    status = Column(String)

    published_book = relationship("Book", back_populates='publisher')

    # def __init__(self, name, country, status=None, founder=None, year_founded=None):
    #     self.name = name
    #     self.founder = founder
    #     self.year_founded = year_founded
    #     self.country = country
    #     self.status = status


"""Publisher stores information abotu a publisher,
it has attributes id, name, date of birth, occupation, nationality
and homepage_URL"""


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_of_birth = Column(Date)
    occupation = Column(String, default="Writer")
    nationality = Column(String)
    homepage_URL = Column(String)

    wrotes_series = relationship(
        "Series",
        secondary=assoc_author_series,
        back_populates="written_by",lazy='dynamic')

    wrotes = relationship(
        "Book",
        secondary=assoc_author_book,
        back_populates="written_by",lazy='dynamic')

    # def __init__(self, name, date_of_birth, occupation = "Writer", nationality = "American", homepage_URL = None):
    #     self.name = name
    #     self.date_of_birth = date_of_birth
    #     self.occupation = occupation
    #     self.nationality = nationality
    #     self.homepage_URL = homepage_URL

