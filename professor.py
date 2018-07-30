class Professor:
    name, name_id = '', ''
    rating, difficulty = 0.0, 0.0
    comments, tags = [], []
    id, num_ratings = 0, 0
    def __init__(self, name, name_id, id, num_ratings, rating="N/A", difficulty="N/A", tags=None, comments=None):
        self.name = name
        self.name_id = name_id
        self.id = id
        self.num_ratings = num_ratings
        self.rating = rating
        self.difficulty = difficulty
        self.tags= tags
        self.comments = comments
