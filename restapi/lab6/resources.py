from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from db import collection
from flasgger import swag_from

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title required', location='json')
parser.add_argument('author', type=str, required=True, help='Author required', location='json')


class BookListResource(Resource):
    @swag_from({
        'tags': ['Books'],
        'description': 'Get all books',
        'responses': {
            200: {
                'description': 'List of books',
                'examples': {
                    'application/json': [{"_id": "507f1f77bcf86cd799439011", "title": "1984", "author": "George Orwell"}]
                }
            }
        }
    })
    def get(self):
        books = list(collection.find())
        for book in books:
            book['_id'] = str(book['_id'])
        return books, 200

    @swag_from({
        'tags': ['Books'],
        'description': 'Add a new book',
        'parameters': [{
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string', 'example': '1984'},
                    'author': {'type': 'string', 'example': 'George Orwell'}
                },
                'required': ['title', 'author']
            }
        }],
        'responses': {
            201: {
                'description': 'Book added',
                'examples': {'application/json': {"message": "Book added", "id": "507f1f77bcf86cd799439011"}}
            },
            400: {'description': 'Invalid input'}
        }
    })
    def post(self):
        try:
            args = parser.parse_args()
            if len(args['title']) > 100 or len(args['author']) > 50:
                return {"message": "Title/author too long"}, 400
            result = collection.insert_one({"title": args['title'], "author": args['author']})
            return {"message": "Book added", "id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 400


class BookResource(Resource):
    @swag_from({
        'tags': ['Books'],
        'description': 'Get book by ID',
        'parameters': [{
            'name': 'book_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Book ID'
        }],
        'responses': {
            200: {
                'description': 'Book data',
                'examples': {'application/json': {"_id": "507f1f77bcf86cd799439011", "title": "1984", "author": "George Orwell"}}
            },
            404: {'description': 'Book not found'},
            400: {'description': 'Invalid ID'}
        }
    })
    def get(self, book_id):
        try:
            book = collection.find_one({"_id": ObjectId(book_id)})
            if not book:
                return {"message": "Book not found"}, 404
            book['_id'] = str(book['_id'])
            return book, 200
        except Exception:
            return {"message": "Invalid ID"}, 400

    @swag_from({
        'tags': ['Books'],
        'description': 'Update book',
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Book ID'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string', 'example': 'New title'},
                        'author': {'type': 'string', 'example': 'New author'}
                    }
                }
            }
        ],
        'responses': {
            200: {'description': 'Book updated', 'examples': {'application/json': {"message": "Book updated"}}},
            404: {'description': 'Book not found'},
            400: {'description': 'Invalid input'}
        }
    })
    def put(self, book_id):
        try:
            args = parser.parse_args()
            result = collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": {"title": args['title'], "author": args['author']}}
            )
            if result.matched_count == 0:
                return {"message": "Book not found"}, 404
            return {"message": "Book updated"}, 200
        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 400

    @swag_from({
        'tags': ['Books'],
        'description': 'Delete book',
        'parameters': [{
            'name': 'book_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Book ID'
        }],
        'responses': {
            200: {'description': 'Book deleted', 'examples': {'application/json': {"message": "Book deleted"}}},
            404: {'description': 'Book not found'},
            400: {'description': 'Invalid ID'}
        }
    })
    def delete(self, book_id):
        try:
            result = collection.delete_one({"_id": ObjectId(book_id)})
            if result.deleted_count == 0:
                return {"message": "Book not found"}, 404
            return {"message": "Book deleted"}, 200
        except Exception:
            return {"message": "Invalid ID"}, 400