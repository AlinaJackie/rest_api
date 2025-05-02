from flask import request, jsonify
from . import db
from .models import Book
from flask import current_app as app

@app.route('/books', methods=['GET'])
def get_books():
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({'error': 'Invalid limit or offset'}), 400

    books = Book.query.limit(limit).offset(offset).all()
    return jsonify([book.to_dict() for book in books]), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author', 'year')):
        return jsonify({'error': 'Missing data'}), 400

    try:
        new_book = Book(title=data['title'], author=data['author'], year=int(data['year']))
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict()), 200

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)

    try:
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
