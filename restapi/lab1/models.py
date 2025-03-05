import uuid
from dataclasses import dataclass, field

@dataclass
class Book:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = field(default="", metadata={"required": True, "max_length": 100})
    author: str = field(default="", metadata={"required": True})

BOOKS_DB = [
    Book(title="Book 1", author="Author 1"),
    Book(title="Book 2", author="Author 2")
]

