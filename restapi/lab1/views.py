from flask import Blueprint, request, jsonify
from .models import BOOKS_DB, Book
from .schemas import BookSchema
from marshmallow.exceptions import ValidationError

main = Blueprint('main', __name__)

@main.route('/v1/api/books', methods=['GET'])
def get_books():
    book_schema = BookSchema(many=True)
    result = book_schema.dump(BOOKS_DB)
    return jsonify(result)

@main.route('/v1/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in BOOKS_DB if book.id == book_id), None)
    if book:
        book_schema = BookSchema()
        return jsonify(book_schema.dump(book))
    return jsonify({"error": "Book not found"}), 404

@main.route('/v1/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book_schema = BookSchema()
    try:
        book = book_schema.load(data)
        BOOKS_DB.append(book)
        return jsonify(book_schema.dump(book)), 201
    except ValidationError as e:
        return jsonify(e.messages), 422

@main.route('/v1/api/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    global BOOKS_DB
    BOOKS_DB = [book for book in BOOKS_DB if book.id != book_id]
    return '', 204
