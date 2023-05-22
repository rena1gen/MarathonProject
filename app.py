from flask import Flask
from flask import render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import random

from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///req.db"
db = SQLAlchemy(app)



class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partname = db.Column(db.String(100), nullable=True)
    bd = db.Column(db.String(100), nullable=True)
    dist = db.Column(db.Float, nullable=True)
    time = db.Column(db.Integer, nullable=True)
    number = db.Column(db.Integer, nullable=True)
    def __str__(self):
        return str(self.number)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def main_page():  # put application's code here
    return render_template('main.html')



@app.route('/reg', methods = ['GET', 'POST'])
def reg():  # put application's code here
    global part
    if request.method == "POST":
        name = request.form['name']
        if len(request.form['name']) == 0:
            flash("Обязательное поле", "Messages")
        bd = request.form['bd']
        time = request.form['time']
        distance = request.form['distance']

        n = random.randint(1001, 10000)
        part = Participant(partname=name, bd=bd, dist=distance, time=time, number=n)


        try:
            print(db.session.add(part))
            db.session.commit()

            return redirect("/successful")

        except:
            return "<h1>Вы не заполнинили форму</h2>"

    else:
        return render_template('regPage.html')


@app.route('/successful')
def success():
    numbers = Participant.query.all()
    last_add = numbers[-1]
    return render_template('success.html', last_add=last_add)

if __name__ == '__main__':
    app.run(debug=True)

