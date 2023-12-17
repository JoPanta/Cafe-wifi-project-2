from flask import Flask, render_template, redirect, url_for
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
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        cafe = Cafe(name=name, map_url=map_url, img_url=img_url, location=location, has_sockets=has_sockets,
                    has_toilet=has_toilet, has_wifi=has_wifi, can_take_calls=can_take_calls, seats=seats, coffee_price=coffee_price)
        db.session.add(cafe)
        db.session.commit()
        return redirect("/")
    return render_template("add.html", form=form)

@app.route("/cafe/<int:cafe_id>")
def show_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return render_template("cafe.html", cafe=cafe)

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect("/")

@app.route('/edit/<int:cafe_id>', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe_to_edit = Cafe.query.get(cafe_id)
    edit_form = AddForm(
        name=cafe_to_edit.name,
        map_url=cafe_to_edit.map_url,
        img_url=cafe_to_edit.img_url,
        location=cafe_to_edit.location,
        seats=cafe_to_edit.seats,
        coffee_price=cafe_to_edit.coffee_price,
        has_sockets=cafe_to_edit.has_sockets,
        has_toilet=cafe_to_edit.has_toilet,
        has_wifi=cafe_to_edit.has_wifi,
        can_take_calls=cafe_to_edit.can_take_calls)
    if edit_form.validate_on_submit():
        cafe_to_edit.name = edit_form.name.data
        cafe_to_edit.map_url = edit_form.map_url.data
        cafe_to_edit.img_url = edit_form.img_url.data
        cafe_to_edit.location = edit_form.location.data
        cafe_to_edit.seats = edit_form.seats.data
        cafe_to_edit.coffee_price = edit_form.coffee_price.data
        cafe_to_edit.has_sockets = edit_form.has_sockets.data
        cafe_to_edit.has_toilet = edit_form.has_toilet.data
        cafe_to_edit.has_wifi = edit_form.has_wifi.data
        cafe_to_edit.can_take_calls = edit_form.can_take_calls.data
        db.session.commit()
        return redirect(url_for("show_cafe", cafe_id=cafe_id))
    return render_template("edit.html", form=edit_form, cafe=cafe_to_edit)



if __name__ == '__main__':
    app.run(debug=True)
