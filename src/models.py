class Author:
    
    def __init__(self, name, surname, country):
        self.name = name,
        self.surname = surname,
        self.country = country

        def get_full_name(self):
            return self.name + " " + self.surname
        
        def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "surname": self.surname,
                "country": self.country
            }
        
        
class Book:
    def __init__(self, title, genre, year, author_id):
        self.title = title,
        self.genre = genre,
        self.year = year,
        self.author_id = author_id
        self.available = True
        
        def get_info(self):
            return self.title + "(" + str(self.year) + ")"
        
        
        def to_dict(self):
            return{
                "id": self.id,
                "title": self.title,
                "genre": self.genre,
                "year": self.year,
                "author_id": self.author_id,
                "available": self.available
            }
            
class Reader:
    def __init__(self, name, email):
        self.name = name,
        self.email = email
        
        def get_info(self):
            return "Читатель: " + self.name + ", Email: " + self.email
        
        def to_dict(self):
            return{
                "id": self.id,
                "name": self.name,
                "email": self.email
            }

class BorrowRecord:
    def __init__(self, book_id, reader_id):
        self.book_id = book_id,
        self.reader_id = reader_id,
        self.borrowed_at = None
        self.returned_at = None
        
        def is_returned(self):
            return self.returned_at is not None
        
        def to_dict(self):
            return {
                "id": self.id,
                "book_id": self.book_id,
                "reader_id": self.reader_id,
                "borrowed_at": str(self.borrowed_at),
                "returned_at": str(self.returned_at) if self.returned_at else None
            }