from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database.connection import (
    connect_to_db,
    get_all_authors, create_author,
    get_all_books, get_book_by_id, create_book,
    create_reader,
    borrow_book, return_book,
    get_books_by_genre, get_reader_stats
)
from src.models.book import Book
from src.models.author import Author
from src.models.reader import Reader

app = FastAPI()

class AuthorCreate(BaseModel):
    name: str
    surname : str
    country: str
    
    
class BookCreate(BaseModel): 
    title: str
    genre: str
    year: int
    author_id: int 

class ReaderCreate(BaseModel):
    name: str
    email: str
    

class BorrowCreate(BaseModel):
    book_id: int
    reader_id: int
    


@app.on_event("startup")
async def startup():
    global conn
    conn = connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    if conn:
        conn.close()
        
        
@app.get("/authors")
def get_auhors():
    try:
        return get_all_authors(conn)
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    
@app.post("/author", status_code=201)
def add_author(data: AuthorCreate):
    try:
        author = Author(data.name, data.surname, data.country)
        result = create_author(conn, author.name, author.surname, author.country)
        if not result:
            raise HTTPException(status_code=500, detail="Ошибка при создании автора")
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server eror")
    


@app.get("/books")
def get_books():
    try:
        return get_all_books(conn)
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/books/{book_id}")
def get_book(book_id: int):
    try:
        book = get_book_by_id(conn, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")

@app.post("/books", status_code=201)
def add_book(data: BookCreate):
    try:
        book = Book(data.title, data.genre, data.year, data.author_id)
        result = create_book(conn, book.title, book.genre, book.year, book.author_id)
        if not result:
            raise HTTPException(status_code=500, detail="Ошибка при создании книги")
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    
    
    
@app.post("/readers", status_code=201)
def add_reader(data: ReaderCreate):
    try:
        reader = Reader(data.name, data.email)
        result = create_reader(conn, reader.name, reader.email)
        if not result:
            raise HTTPException(status_code=500, detail="Ошибка при создании читателя")
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    
    
    
@app.post("/borrow", status_code=201)
def borrow(data: BorrowCreate):
    try:
        result = borrow_book(conn, data.book_id, data.reader_id)
        if not result:
            raise HTTPException(status_code=400, detail="Книга недоступна или не найдена")
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")

@app.put("/borrow/{record_id}/return")
def return_borrowed(record_id: int):
    try:
        result = return_book(conn, record_id)
        if not result:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    
    
    
@app.get("/stats/genres")
def stats_genres():
    try:
        return get_books_by_genre(conn)
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")

@app.get("/stats/readers")
def stats_readers():
    try:
        return get_reader_stats(conn)
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
        