import pickle
import os
from models import Base, Author, Book, Series, Publisher
import re
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#/u/yipuwang/cs373-idb/flaskapp/data/authors_table.p"
AUTHORS_PATH = "/u/yipuwang/cs373-idb/flaskapp/data/authors_table.p"
BOOKS_PATH = "/u/yipuwang/cs373-idb/flaskapp/data/books_table.p"
PUBLISHERS_PATH = "//u/yipuwang/cs373-idb/flaskapp/data/publisher_table.p"
SERIES_PATH = "/u/yipuwang/cs373-idb/flaskapp/data/gr_series.p"
SERIES_AUTHOR_PATH = "/u/yipuwang/cs373-idb/flaskapp/data/gr_authors.p"
SERIES_BOOK_PATH = "/u/yipuwang/cs373-idb/flaskapp/data/gr_books.p"

"""
Author:
name, date_of_birth, occupation, nationality, homepage_URL, book_list

Book:
title, isbn, written_by, publisher, image_link

Publisher:
name, founder, year_founded, country, status

Series:
title, gnere, num_books, status
"""

authors = []
books = []
publishers = []
series = []
series_authors = []
series_books = []
aus = {}
pus = {}
isbn = {}	

def read ():
	global authors
	global books
	global publishers
	if os.path.isfile(AUTHORS_PATH):
		au = open(AUTHORS_PATH, 'rb')
		authors = pickle.load(au)
		au.close()
	else:
		print("Reading authors FAILED !!!!!!")

	if os.path.isfile(BOOKS_PATH):
		bo = open(BOOKS_PATH, 'rb')
		books = pickle.load(bo)
		bo.close()
	else:
		print("Reading books FAILED !!!!!!")

	if os.path.isfile(PUBLISHERS_PATH):
		pu = open(PUBLISHERS_PATH, 'rb')
		publishers = pickle.load(pu)
		pu.close()
	else:
		print("Reading publishers FAILED !!!!!!")

	# if os.path.isfile(SERIES_PATH):
	# 	se = open(SERIES_PATH, 'rb')
	# 	series = pickle.load(se)
	# 	se.close()
	# else:
	# 	print("Reading series FAILED !!!!!!")
			
	if os.path.isfile(SERIES_AUTHOR_PATH):
		sa = open(SERIES_AUTHOR_PATH, 'rb')
		series_authors = pickle.load(sa)
		sa.close()
	else:
		print("Reading series FAILED !!!!!!")

	if os.path.isfile(SERIES_PATH):
		sb = open(SERIES_BOOK_PATH, 'rb')
		series_books = pickle.load(sb)
		sb.close()
	else:
		print("Reading series FAILED !!!!!!")


def load ():
	global aus
	global pus
	global isbn	
	engine = create_engine('sqlite:////u/yipuwang/cs373-idb/flaskapp/data/test.db', echo=True)
	# engine = create_engine('postgresql://testdb:servicerequested@localhost:5432/testdb', echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()
	engine.execute('DROP TABLE IF EXISTS authors;')
	engine.execute('DROP TABLE IF EXISTS books;')
	engine.execute('DROP TABLE IF EXISTS series;')
	engine.execute('DROP TABLE IF EXISTS publishers;')
	engine.execute('DROP TABLE IF EXISTS assoc_author_book;')
	engine.execute('DROP TABLE IF EXISTS assoc_author_series;')
	# Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	for author in authors:
		# print(author.keys())
		author_db_format = Author(
			name = author['name'],
			date_of_birth = author['date_of_birth'],
			nationality = author['nationality'],
			homepage_URL = author['homepage_url'],
			occupation = author['occupation'],
			image = author['image']
			)
		aus[author_db_format.name] = author_db_format


	for publisher in publishers:
		publisher_db_format = Publisher(
			name = publisher["name"],
			founder = publisher["founder"],
			year_founded = publisher["year_founded"],
			country = publisher["country"],
			status = publisher["status"],
			image = publisher['image']

			)		
		pus[publisher_db_format.name] = publisher_db_format
		session.add(publisher_db_format)

	for book in books:
		book_db_format = Book(
			title = book["title"],
			isbn = book["isbn"],
			image_link = book['image_link'],
			description = book['description'],	
			amazon_product_url = book['amazon_url']
			)
		# print(book.keys())
		if book_db_format.isbn not in isbn:
			if book['written_by'] != '' and book['written_by'] in aus and book['publisher'] in pus:
				book_db_format.written_by = [aus[book['written_by']]]
				isbn[book_db_format.isbn] =  book_db_format
				book_db_format.publisher = pus[book['publisher']]
				session.add(book_db_format)




	session.commit()
	session.close()



def load_series():
	ser = {}
	engine = create_engine('sqlite:////u/yipuwang/cs373-idb/flaskapp/data/test.db', echo=True)
	# engine = create_engine('postgresql://testdb:servicerequested@localhost:5432/testdb', echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()
	for serie in series:
		status = 1
		if serie["numbered"]:
			status = 0
		db_format = Series(
			title = serie["title"],
			num_books = serie["num_books"],
			description = serie["description"],
			notes = serie["notes"],
			status = status,
			)		
		ser[db_format.name] = db_format
		session.add(db_format)
	
	for book in series_books:
		db_format = Book(
			title = book['title'],
			isbn = book['isbn'],
			image_link = book["img"],)


def main():
    read()
    # load()


if __name__ == "__main__":
    main()
