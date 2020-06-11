from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://stzkshjhxfkscz:1d9b2c121c6102f07b9ed80eeb5d4f20906fb8a440a88e4c361fb521bdbac355@ec2-174-129-255-76.compute-1.amazonaws.com:5432/dfk323c6tcrghi"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    brokerage = db.Column(db.String(100))
    state = db.Column(db.String(2))
    city = db.Column(db.String(100))
    post_code = db.Column(db.String(5))
    phone = db.Column(db.String(13))
    realtor_email = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    rating = db.Column(db.Float)
    review = db.Column(db.Text)

    def __init__(self, first_name, last_name, brokerage, state, city, post_code, phone, realtor_email, user_email, rating, review):
        self.first_name = first_name
        self.last_name = last_name
        self.brokerage = brokerage
        self.state = state
        self.city = city
        self.post_code = post_code
        self.phone = phone
        self.realtor_email = realtor_email
        self.user_email = user_email
        self.rating = rating
        self.review = review

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'brokerage', 'state', 'city', 'post_code', 'phone', 'realtor_email', 'user_email', 'rating', 'review')

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@app.route('/review', methods=["POST"])
def add_review():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    brokerage = request.json['brokerage']
    state = request.json['state']
    city = request.json['city']
    post_code = request.json['post_code']
    phone = request.json['phone']
    realtor_email = request.json['realtor_email']
    user_email = request.json['user_email']
    rating = request.json['rating']
    review = request.json['review']

    new_review = Review(first_name, last_name, brokerage, state, city, post_code, phone, realtor_email, user_email, rating, review)

    db.session.add(new_review)
    db.session.commit()

    item = Review.query.get(new_review.id)

    return review_schema.jsonify(item)

@app.route('/reviews', methods=["GET"])
def get_reviews():
    all_reviews = Review.query.all()
    result = reviews_schema.dump(all_reviews)
    return jsonify(result)

@app.route('/review/<id>', methods=["GET"])
def get_review(id):
    item = Review.query.get(id)
    return review_schema.jsonify(item)

@app.route('/review/<id>', methods=["PUT"])
def update_review(id):
    item = Review.query.get(id)
    item.first_name = request.json['first_name']
    item.last_name = request.json['last_name']
    item.brokerage = request.json['brokerage']
    item.state = request.json['state']
    item.city = request.json['city']
    item.post_code = request.json['post_code']
    item.phone = request.json['phone']
    item.realtor_email = request.json['realtor_email']
    item.user_email = request.json['user_email']
    item.rating = request.json['rating']
    item.review = request.json['review']

    db.session.commit()
    return review_schema.jsonify(item)

@app.route('/review/remove/<id>', methods=["DELETE"])
def delete_review(id):
    item = Review.query.get(id)
    db.session.delete(item)
    db.session.commit()

    return review_schema.jsonify(item)

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
emails_schema = EmailSchema(many=True)

@app.route("/emails", methods=["GET"])
def get_emails():
    all_emails = Email.query.all()
    result = emails_schema.dump(all_emails)
    return jsonify(result)

@app.route("/email/<id>", methods=["GET"])
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