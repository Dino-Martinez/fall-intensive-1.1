""" This project will allow people to easily find a tutor near them, in
    their desired subject/grade level; it will also allow them to
    communicate with said tutor, and possibly allow for secure payment
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tutorsDatabase"
mongo = PyMongo(app)
db = mongo.db


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tutors')
def tutors():
    if len(request.args) == 0:
        # display all tutors
        tutors = db.tutors.find({})
    else:
        # display sorted results
        criteria = request.args.get('field-one').lower()
        sort_choice = request.args.get('sort-order').lower()
        sort_direction = 1
        if (sort_choice == 'descending'):
            sort_direction = -1
        tutors = db.tutors.find({}).sort(criteria, sort_direction)

    context = {
        'tutors': tutors
    }

    return render_template('tutors.html', **context)


@app.route('/tutors/<tutor_id>')
def one_tutor(tutor_id):
    tutor = db.tutors.find_one({'_id': ObjectId(tutor_id)})

    return render_template('tutor.html', **tutor)


@app.route('/register_tutor', methods=["GET", "POST"])
def add_tutor():
    if request.method == "POST":
        tutor = {
            "name": request.form.get('name'),
            "age": request.form.get('age'),
            "subject": request.form.get('subject'),
            "level": request.form.get('level'),
            "in_person": request.form.get('in-person'),
            "virtual": request.form.get('virtual')
        }

        inserted = db.tutors.insert_one(tutor)

        print(inserted)

        return redirect(url_for('add_tutor'))
    else:
        return render_template('add_tutor.html')


@app.route('/remove_tutor/<tutor_id>')
def delete_tutor(tutor_id):
    db.tutors.delete_one({'_id': ObjectId(tutor_id)})
    return redirect(url_for('tutors'))


@app.route('/coming_soon')
def coming_soon():
    return render_template('coming_soon.html')


if __name__ == '__main__':
    app.run(debug=True)
