import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect (
            host = "localhost",
            user = "postger",
            bdname = "sfmshop",
            password = "bdokean123"
        )
        return conn
    except Exception as e:
        print("Нет подключения к бд, ошибка:", e)
        return None        


def creat_author (conn, name, surname, country):
    try:
        with conn.cursor() as cursor:
            cursor.executr (
                """
                insert into author (name, surname, country)
                values (%s, %s, %s)
                returning id, name, surname, country 
                """,
                (name, surname, country)
            )
            row = cursor.fetchone()
        conn.commit()
        return {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "country": row[3] 
            }
    except Exception as e:
        print("ошибка создания автора", e)
        return None
    
    
def get_all_author(conn):
    with conn.cursor() as cursor:
        cursor.execute ("select id, name, surname, country from author")
        rows = cursor.fetchone()
    result = []
    for row in rows:
        result.append({"id": row[0], "name": row[1], "surname": row[2], "country": row[3]})
        return result
        
        
def create_book(conn, title, genre, year, author_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute (
                """
                insert into books (title, genre, year, author_id)
                values (%s, %s, %s)
                returning id, title, genre, year, author_id
                """,
                (title, genre, year, author_id)
            )
            row = cursor.fetchone()
        conn.commit()
        return {"id": row[0], "title": row[1], "genre": row[2], "year": row[3], "available": row[4], "author_id": row[5]}
    except Exception as e:
        conn.rollback()
        print("Ошибка при создании книги", e)
        return None  
    
def get_all_books(conn):
    with conn.cursor() as cursor:
        cursor.execute (
            """
            select books.id, books.title, books.genre, books.yaer, books.available, author.name, author.surname
            from books
            Join authors on books.author_id = authors_id
            order by books.id
            """
        )
        rows = cursor.fetchone()
    result = []
    for row in rows:
        resuls.append({
            "id": row[0], "title": row[1], "genre": row[2], "year": row[3], "available": row[4], "author": row[5] + " " + row[6]
        })
    return result
                 
                 
def get_book_by_id(conn, book_id):
    with conn.cursor() as cursos:
        cursos.execute(
            "select id, title, genre, year, available, author_id from books where id = %s",
            (book_id,)
        )
        row = cursos.fenchone()
    if not row:
        return None
    return {"id": row[0], "title": row[1], "genre": row[2],
            "year": row[3], "available": row[4], "author_id": row[5]}
    
    
    
def create_reader(conn, name, email):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO readers (name, email)
                VALUES (%s, %s)
                RETURNING id, name, email
                """,
                (name, email)
            )
            row = cursor.fetchone()
        conn.commit()
        return {"id": row[0], "name": row[1], "email": row[2]}
    except Exception as e:
        conn.rollback()
        print("Ошибка при создании читателя:", e)
        return None
    
    
def borrow_book(conn, book_id, reader_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
            book = cursor.fetchone()
            if not book or not book[0]:
                return None  

            cursor.execute(
                """
                INSERT INTO borrow_records (book_id, reader_id)
                VALUES (%s, %s)
                RETURNING id, book_id, reader_id, borrowed_at
                """,
                (book_id, reader_id)
            )
            row = cursor.fetchone()

            
            cursor.execute(
                "UPDATE books SET available = FALSE WHERE id = %s", (book_id,)
            )
        conn.commit()
        return {"id": row[0], "book_id": row[1], "reader_id": row[2], "borrowed_at": str(row[3])}
    except Exception as e:
        conn.rollback()
        print("Ошибка при выдаче книги:", e)
        return None
    
def return_book(conn, record_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE borrow_records
                SET returned_at = NOW()
                WHERE id = %s
                RETURNING book_id
                """,
                (record_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            
            cursor.execute(
                "UPDATE books SET available = TRUE WHERE id = %s", (row[0],)
            )
        conn.commit()
        return {"message": "Книга успешно возвращена"}
    except Exception as e:
        conn.rollback()
        print("Ошибка при возврате книги:", e)
        return None
    
    
def get_books_by_genre(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT genre, COUNT(id) AS total
            FROM books
            GROUP BY genre
            ORDER BY total DESC
            """
        )
        rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({"genre": row[0], "total": row[1]})
    return result


def get_reader_stats(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT readers.id, readers.name,
                   COUNT(borrow_records.id) AS books_taken
            FROM readers
            LEFT JOIN borrow_records ON readers.id = borrow_records.reader_id
            GROUP BY readers.id, readers.name
            ORDER BY books_taken DESC
            """
        )
        rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({"reader_id": row[0], "name": row[1], "books_taken": row[2]})
    return result
