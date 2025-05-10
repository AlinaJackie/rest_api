swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Library API",
        "description": "API for book management using Flask-RESTful and MongoDB. Swagger documentation.",
        "version": "1.0.0",
        "contact": {
            "name": "alina",
            "email": "alina.baran.22@pnu.edu.ua"
        }
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {
            "name": "Books",
            "description": "Book operations"
        }
    ]
}