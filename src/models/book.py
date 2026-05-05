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