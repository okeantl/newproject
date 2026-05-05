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
   