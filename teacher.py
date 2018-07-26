class Teacher:
    name = ''
    rating = 0.0
    difficulty = 0.0
    comments = []
    def __init__(self, name, rating, difficulty, comments):
        self.name = name
        self.rating = rating
        self.difficulty = difficulty
        self.comments = comments
