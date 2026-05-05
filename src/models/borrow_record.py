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