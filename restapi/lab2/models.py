import uuid

class Book:
    def __init__(self, title: str, author: str, year: int):
        self.id = str(uuid.uuid4())  # Генерація унікального ID
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author, "year": self.year}
