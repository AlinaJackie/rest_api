from flask import request, jsonify
from . import db
from .models import Book
from flask import current_app as app
from datetime import datetime


@app.route('/books', methods=['GET'])
def get_books():
    try:
        limit = int(request.args.get('limit', 10))
        cursor = request.args.get('cursor')
    except ValueError:
        return jsonify({'error': 'Invalid parameters'}), 400

    query = Book.query.order_by(Book.created_at.desc(), Book.id.desc())

    if cursor:
        try:
            cursor_time = datetime.fromisoformat(cursor)
            query = query.filter(Book.created_at < cursor_time)
        except ValueError:
            return jsonify({'error': 'Invalid cursor format'}), 400

    books = query.limit(limit).all()

    next_cursor = books[-1].created_at.isoformat() if books else None

    return jsonify({
        'books': [book.to_dict() for book in books],
        'next_cursor': next_cursor
    }), 200


# Інші ендпоінти залишаються без змін
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