from fastapi import APIRouter, HTTPException
from schemas import BookSchema
from database import BOOKS_DB
from models import Book
from typing import List

router = APIRouter()


@router.get("/books/", response_model=List[dict])
async def get_books():
    return [book.to_dict() for book in BOOKS_DB]


@router.get("/books/{book_id}", response_model=dict)
async def get_book(book_id: str):
    book = next((book for book in BOOKS_DB if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail={"error": "Book not found"})
    return book.to_dict()


@router.post("/books/", response_model=dict, status_code=201)
async def create_book(book: BookSchema):
    new_book = Book(**book.dict())
    BOOKS_DB.append(new_book)
    return new_book.to_dict()


@router.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: str):
    global BOOKS_DB
    book = next((book for book in BOOKS_DB if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail={"error": "Book not found"})

    BOOKS_DB = [b for b in BOOKS_DB if b.id != book_id]
    return {"message": "Book deleted successfully"}
