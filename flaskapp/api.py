import subprocess
import flask.ext.sqlalchemy
from flask import jsonify, request, make_response
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import Book, Author, Publisher, Series

app = flask.Flask(__name__)
"""
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////u/kh1994/cs373-idb/flaskapp/data/test.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)
"""

#engine = create_engine('sqlite:////u/kh1994/cs373-idb/flaskapp/data/test.db', echo=True)
engine = create_engine('postgresql://testdb:servicerequested@localhost:5432/testdb', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

"""
GET BOOKS
"""
@app.route('/api/books', methods = ['GET'])
def get_books():
    book_id = request.args.get('id') if request.args.get('id') is not None else -1
    book_title = request.args.get('title') if request.args.get('title') is not None else None
    book_isbn = request.args.get('isbn') if request.args.get('isbn') is not None else None

    book = None

    """Examine the arguements"""
    if(book_id != -1):
        book = session.query(Book).get(book_id)
    elif(book_title):
        book = session.query(Book).filter(Book.title.ilike(book_title)).first()
    elif(book_isbn):
        book = session.query(Book).filter_by(isbn=book_isbn).first()
    else:
        try:
            all_books = session.query(Book).all()
            titles = [(b.id, b.title) for b in all_books]
            return jsonify(titles)
        except:
            session.rollback()
            not_found(404)

    if(book):
        b_authors = [(a.id, a.name) for a in book.written_by]
        b_pub = (book.publisher.id, book.publisher.name) if book.publisher is not None else " "
        b_series = (book.in_series.id, book.in_series.title) if book.in_series is not None else " "

        return jsonify({'id': book.id, 'title': book.title, 'author': b_authors, 'isbn-13': book.isbn, 'publisher': b_pub, 
            'in_series': b_series, 'description': book.description, 'amazon_product_url': book.amazon_product_url, 'image_url': book.image_link})
    else: 
        return not_found(404)

"""
GET AUTHORS
"""
@app.route('/api/authors')
def get_authors():
    auth_id = request.args.get('id') if request.args.get('id') is not None else -1
    auth_name = request.args.get('name') if request.args.get('name') is not None else None
    author = None

    if(auth_id != -1):
        author = session.query(Author).get(auth_id)
    elif(auth_name):
        author = session.query(Author).filter(Author.name.ilike(auth_name)).first()
    else:
        all_auth = session.query(Author).all()
        names = [(a.id, a.name) for a in all_auth]
        return jsonify(names)

    if(author):
        a_books = [(b.id, b.title) for b in author.wrotes]

        return jsonify({'id': author.id, 'name': author.name, 'date_of_birth': author.date_of_birth, 'occupation': author.occupation, 
                'nationality': author.nationality, 'books_written': a_books, 'website': author.homepage_URL,
                'image_url': author.image})
    else: 
        return not_found(404)

"""
GET PUBLISHERS
"""
@app.route('/api/publishers')
def get_publishers():
    pub_id = request.args.get('id') if request.args.get('id') is not None else -1
    pub_name = request.args.get('name') if request.args.get('name') is not None else None
    publisher = None

    #   Publisher ID
    if(pub_id != -1):
        publisher = session.query(Publisher).get(pub_id)
    #   Publisher Name
    elif(pub_name):
        publisher = session.query(Publisher).filter(Publisher.name.ilike(pub_name)).first()
    #   Return list of all publisher names
    else:
        all_pub = session.query(Publisher).all()
        names = [(p.id, p.name) for p in all_pub]
        return jsonify(names)

    #   Tests if specific publisher given exists or not
    if(publisher):
        p_books = [(b.id, b.title) for b in publisher.published_book]
        return jsonify({'id': publisher.id, 'name': publisher.name, 'founder': publisher.founder, 'year_founded': publisher.year_founded, 
            'country': publisher.country, 'status': publisher.status, 'published_books': p_books, 'logo': publisher.image})
    else:
        return not_found(404)


"""
GET SERIES
"""
@app.route('/api/series')
def get_series():
    series_id = request.args.get('id') if request.args.get('id') is not None else -1
    series_title = request.args.get('title') if request.args.get('title') is not None else None

    #   Series ID
    if(series_id != -1):
        series = session.query(Series).get(series_id)
    #   Series Title
    elif(series_title):
        series = session.query(Series).filter(Series.name.ilike(series_title)).first()
    #   Returns list of all series names
    else:
        all_series = session.query(Series).all()
        titles = [(s.id, s.title) for s in all_series]
        return jsonify(titles)

    if(series):
        s_authors = [(a.id, a.name) for a in series.written_by]
        s_books = [(b.id, b.title) for b in series.books]
        return jsonify({'id': series.id, 'title': series.title, 'genre': series.genre, 'num_books': series.num_books, 
            'status': series.status, 'author': s_author, 'books_in_series': s_books})
    else:
        return not_found(404)
   
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(debug=True)
