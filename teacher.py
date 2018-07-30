class Teacher:
    name, name_id = '', ''
    rating, difficulty = 0.0, 0.0
    comments, tags = [], []
    id = 0
    def __init__(self, name, name_id, id, rating="N/A", difficulty="N/A", tags=None, comments=None):
        self.name = name
        self.name_id = name_id
        self.id = id
        self.rating = rating
        self.difficulty = difficulty
        self.tags= tags
        self.comments = comments
