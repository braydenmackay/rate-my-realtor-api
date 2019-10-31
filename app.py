from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask-marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://oyamnpeoairmqc:dd0f39416d6e2b98fb249f501738f595b8d17240c54843cc7645ab8e2a5ffe03@ec2-23-21-94-99.compute-1.amazonaws.com:5432/d7s4qffordvktr"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    rating = db.Column(db.Interger)
    brokerage = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    review = db.Column(db.Blob)

    def __init__(self, name, rating, brokerage, city, state, review):
        self.name = name
        self.rating = rating
        self.brokerage = brokerage
        self.city = city
        self.state = state
        self.review = review

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "rating", "brokerage", "city", "state", "review")

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@app.route("/reviews", methods=["GET"])
def get_reviews():
    all_reviews = Review.query.all()
    result = reviews_schema.dump(all_reviews)
    return jsonify(result)

@app.route("/reviews/<id>", methods=["GET"])
def get_review(id):
    review = Review.query.get(id)
    result = review_schema.dump(review)
    return jsonify(result)

@app.route("/review", methods=["POST"])
def add_review():
    name = request.json["name"]
    rating = request.json["rating"]
    brokerage = request.json["brokerage"]
    city = request.json["city"]
    state = request.json["state"]
    review = request.json["review"]

    new_review = Review(name, rating, brokerage, city, state, review)
    db.session.add(new_review)
    db.session.commit()

    created_review = Review.query.get(new_review.id)
    return review_schema.jsonify(created_review)

@app.route("/review/<id>", methods=["PUT"])
def update_review(id):
    review = Review.query.get(id)

    review.name = request.json["name"]
    review.rating = request.json["rating"]
    review.brokerage = request.json["brokerage"]
    review.city = request.json["city"]
    review.state = request.json["state"]
    review.review = request.json["review"]

    db.session.commit()
    return review_schema.jsonify(review)

@app.route("/review/<id>", methods=["DELETE"])
def delete_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()

    return "REVIEW DELETED"

class Email(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(25))
    last = db.Column(db.String(25))
    email = db.Column(db.String(100))

    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email

class EmailSchema(ma.Schema):
    class Meta:
        fields = ("id", "first", "last", "email")

email_schema = EmailSchema()
email_schema = EmailSchema(many=True)

@app.route("/emails", methods=["GET"])
def get_email():
    all_emails = Email.query.all()
    result = emails_schema.dump(all_emails)
    return jsonify(result)

@app.route("/reviews/<id>", methods=["GET"])
def get_email(id):
    email = Email.query.get(id)
    result = email_schema.dump(email)
    return jsonify(result)

@app.route("/email", methods=["POST"])
def add_email():
    first = request.json["first"]
    last = request.json["last"]
    email = request.json["email"]

    new_email = Email(first, last, email)
    db.session.add(new_email)
    db.session.commit()

    created_email = Email.query.get(new_email.id)
    return email_schema.jsonify(created_email)

@app.route("/email/<id>", methods=["DELETE"])
def delete_email(id):
    email = Email.query.get(id)
    db.session.delete(email)
    db.session.commit()

    return "EMAIL DELETED"

if __name__ == "__main__":
    app.debug = True
    app.run()