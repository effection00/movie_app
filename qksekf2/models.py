from qksekf import db

class Comment(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))

    def __repr__(self):
        return f"Comment {self.id}"


class Movie(db.Model):
    __tablename__="movie" #tablename 필수 
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String)
    review_text = db.Column(db.String)
    review_star = db.Column(db.Integer)
    def __repr__(self):
        return f"movie {self.id}"

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.String, primary_key=True, nullable= False, unique=True)
    email = db.Column(db.String, nullable= False, unique=True)
    nickname = db.Column(db.String, nullable= False, unique=True)
    pw = db.Column(db.String, nullable= False)
    def __repr__(self):
        return f"user {self.id}"


class Mymovie(db.Model):
    __tablename__='mymovie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"user {self.title}"
