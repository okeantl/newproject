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