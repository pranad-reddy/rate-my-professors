"""
Contains definition of Professor class
"""


class Professor:
    """
    Object to hold professor data. __init__ method sets object attributes to specified argument values
    Args:
        name (str): professor name
        name_id (str): professor name in format as seen on berkeleytime.com
        id (int): unique professor identifier on ratemyprofessors.com
        num_ratings (int): total number of ratings
        rating (float): rating / 5/0
        difficulty (float): difficulty / 5
        tags (list): top 3 tags voted to identify professor with
        comments (list): top 20 (max) comments for professor
    Attributes: (same as Args)
    """
    name, name_id = '', ''
    rating, difficulty = 0.0, 0.0
    comments, tags = [], []
    id, num_ratings = 0, 0

    def __init__(self, name, name_id, id, num_ratings, rating=-1.0, difficulty=-1.0, tags=None, comments=None):
        self.name = name
        self.name_id = name_id
        self.id = id
        self.num_ratings = num_ratings
        self.rating = rating
        self.difficulty = difficulty
        self.tags = tags
        self.comments = comments
