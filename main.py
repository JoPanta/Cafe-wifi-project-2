from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretcode'
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),  nullable=False)
    map_url = db.Column(db.String(500),  nullable=False)
    img_url = db.Column(db.String(250),  nullable=False)
    location = db.Column(db.String(250),  nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("index.html", cafes=cafes)

class AddForm(FlaskForm):
    name = StringField("Place Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    location = StringField("Location Address", validators=[DataRequired()])

    seats = SelectField(label="Number of Seats", choices=[("0-10", "0-10"), ("10-20", "10-20"),
                                                          ("20-30", "20-30"), ("30-40", "30-40"),
                                                          ("40-50", "40-50"), ("50+", "50+")], validators=[DataRequired()])
    coffee_price = StringField("Coffee Price (Lbs)", validators=[DataRequired()])
    has_sockets = BooleanField("Power Sockets Available?")
    has_toilet = BooleanField("Toilet Facilities Available?")
    has_wifi = BooleanField("Wi-Fi Available?")
    can_take_calls = BooleanField("Accepts Phone Calls?")
    submit = SubmitField("Submit")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        mpa_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        cafe = Cafe(name=name, map_url=mpa_url, img_url=img_url, location=location, has_sockets=has_sockets,
                    has_toilet=has_toilet, has_wifi=has_wifi, can_take_calls=can_take_calls, seats=seats, coffee_price=coffee_price)
        db.session.add(cafe)
        db.session.commit()
        return redirect("/")
    return render_template("add.html", form=form)





if __name__ == '__main__':
    app.run(debug=True)
