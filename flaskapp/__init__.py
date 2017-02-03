#!/usr/bin/env python

import subprocess

from flask import Flask, render_template, jsonify, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Author, Book, Series, Publisher
from api import get_books, get_authors, get_publishers, get_series, not_found

app = Flask(__name__)

# engine = create_engine('sqlite:////u/kh1994/cs373-idb/flaskapp/data/test.db', echo=True)
engine = create_engine('postgresql://testdb:servicerequested@localhost:5432/testdb', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/books')
def bookspage():
    books = session.query(Book).yield_per(10).enable_eagerloads(False)

    return render_template('bookspage.html', books=books)


@app.route('/authors')
def authorspage():
    authors = session.query(Author).all()

    return render_template('authorspage.html', authors=authors)


@app.route('/publishers')
def publisherspage():
    publishers = session.query(Publisher).all()

    return render_template('publisherspage.html', publishers=publishers)


@app.route('/series')
def seriespage():
    return render_template('seriespage.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/books/<int:id>')
def book_page(id):
    book = session.query(Book).get(id)

    return render_template('book_details.html', book=book)


@app.route('/authors/<int:id>')
def author_page(id):
    author = session.query(Author).get(id)

    return render_template('author_details.html', author=author)


@app.route('/series/<int:id>')
def series_page(id):
    url = 'series' + str(id) + '.html'
    return render_template(url)


@app.route('/publishers/<int:id>')
def publisher_page(id):
    publisher = session.query(Publisher).get(id)

    return render_template('publisher_details.html', publisher=publisher)


@app.route('/api/run_tests')
def api_run_tests():
    try:
        test_results = subprocess.check_output("/var/www/flaskapp/flaskapp/tests.py", stderr=subprocess.STDOUT)
        return test_results
    except Exception as e:
        return str(e)

@app.route('/api/<string:restful>')
def restful_api(restful):
    if restful == 'books':
        return get_books()
    elif restful == 'authors':
        return get_authors()
    elif restful == 'publishers':
        return get_publishers()
    elif restful == 'series':
        return get_series()
    else:
        return not_found(404)



"""
----
RESTFUL API 
----

#GET BOOKS

@app.route('/api/books', methods = ['GET'])
def get_books():
    book_id = request.args.get('id') if request.args.get('id') is not None else -1
    book_title = request.args.get('title') if request.args.get('title') is not None else None
    book_isbn = request.args.get('isbn') if request.args.get('isbn') is not None else None

    #Examine the arguements
    #   Book ID
    if(book_id != -1):
        book = session.query(Book).get(book_id)
        if(book):
            b_authors = [a.name for a in book.written_by]
            b_pub = book.publisher.name if book.publisher is not None else " "
            b_series = book.in_series.title if book.in_series is not None else " "

            return jsonify({'title': book.title, 'author': b_authors, 'isbn': book.isbn, 'publisher': b_pub, 
                'in_series': b_series})
        else: 
            not_found(404)
    #   Book Title
    elif(book_title):
        book = session.query(Book).filter_by(title=book_title.upper()).first()
        if(book):
            b_authors = [a.name for a in book.written_by]
            b_pub = book.publisher.name if book.publisher is not None else " "
            b_series = book.in_series.title if book.in_series is not None else " "

            return jsonify({'title': book.title, 'author': b_authors, 'isbn': book.isbn, 'publisher': book.publisher.name, 
                'in_series': book.in_series.title})
        else: 
            not_found(404)
    #   Book ISBN-13
    elif(book_isbn):
        book = session.query(Book).filter_by(isbn=book_isbn).first()
        if(book):
            b_authors = [a.name for a in book.written_by]
            b_pub = book.publisher.name if book.publisher is not None else " "
            b_series = book.in_series.title if book.in_series is not None else " "

            return jsonify({'title': book.title, 'author': b_authors, 'isbn': book.isbn, 'publisher': book.publisher.name, 
                'in_series': book.in_series.title})
        else: 
            not_found(404)

    #Print all books titles if no arguments
    all_books= session.query(Book).all()
    titles = (b.title for b in all_books)
    return jsonify(titles)


#GET AUTHORS

@app.route('/api/authors')
def get_authors():
    auth_id = request.args.get('id') if request.args.get('id') is not None else -1
    auth_name = request.args.get('name') if request.args.get('name') is not None else None

    #Examine the arguements
    #   Author ID
    if(auth_id != -1):
        author = session.query(Author).get(auth_id)
        if(author):
            a_books = [b.title for b in author.wrotes]
            a_series = [s.title for s in author.wrotes_series]

            return jsonify({'name': author.name, 'date_of_birth': author.date_of_birth, 'occupation': author.occupation, 
                'nationality': author.nationality, 'books_written': a_books, 'series_written': a_series})
        else: 
            not_found(404)

    #   Author Name
    elif(auth_name):
        author = session.query(Author).filter_by(name=auth_name).first()
        if(author):
            a_books = [b.title for b in author.wrotes]
            a_series = [s.title for s in author.wrotes_series]

            return jsonify({'name': author.name, 'date_of_birth': author.date_of_birth, 'occupation': author.occupation, 
                'nationality': author.nationality, 'books_written': a_books, 'series_written': a_series})
        else: 
            not_found(404)
    
    #Print all authors names if no arguments
    all_auth = session.query(Author).all()
    names = [a.name for a in all_auth]
    return jsonify(names)


#GET PUBLISHERS

@app.route('/api/publishers')
def get_publishers():
    pub_id = request.args.get('id') if request.args.get('id') is not None else -1
    pub_name = request.args.get('name') if request.args.get('name') is not None else None

   #Examine the arguments
    #   Publisher ID
    if(pub_id != -1):
        publisher = session.query(Publisher).get(pub_id)
        if(publisher):
            p_books = [b.title for b in publisher.published_books]
            return jsonify({'name': publisher.name, 'founder': publisher.founder, 'year_founded': publisher.year_founded, 
                'country': publisher.country, 'status': publisher.status, 'published_books': p_books})
        else:
            not_found(404)

    #   Publisher Name
    elif(pub_name):
        publisher = session.query(Publisher).filter_by(name=pub_name).first()
        if(publisher):
            p_books = [b.title for b in publisher.published_books]
            return jsonify({'name': publisher.name, 'founder': publisher.founder, 'year_founded': publisher.year_founded, 
                'country': publisher.country, 'status': publisher.status, 'published_books': p_books})
        else:
            not_found(404)

    #Print all publisher names if no arguments
    all_pub = session.query(Publisher).all()
    names = [p.name for p in all_pub]
    return jsonify(names)


#GET SERIES

@app.route('/api/series')
def get_series():
    series_id = request.args.get('id') if request.args.get('id') is not None else -1
    series_title = request.args.get('title') if request.args.get('title') is not None else None

    #Examine the arguments
    #   Series ID
    if(series_id != -1):
        series = session.query(Series).get(series_id)
        if(series):
            s_authors = [a.name for a in series.written_by]
            s_books = [b.title for b in series.books]
            return jsonify({'title': series.title, 'genre': series.genre, 'num_books': series.num_books, 
                'status': series.status, 'author': s_author, 'books_in_series': s_books})
        else:
            not_found(404)
    #   Series Title
    elif(series_title):
        series = session.query(Series).filter_by(title=series_title).first()
        if(series):
            s_authors = [a.name for a in series.written_by]
            s_books = [b.title for b in series.books]
            return jsonify({'title': series.title, 'genre': series.genre, 'num_books': series.num_books, 
                'status': series.status, 'author': s_author, 'books_in_series': s_books})
        else:
            not_found(404)

    #Print all series if no arguments
    all_series = session.query(Series).all()
    titles = [s.title for s in all_series]
    return jsonify(titles)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
"""

if __name__ == "__main__":
    app.run(debug=True)
