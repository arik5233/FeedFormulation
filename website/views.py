from flask import Blueprint, render_template , request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import data as data
from .calculate import calculate_feed

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/calculate', methods=['GET', 'POST'])
def calculate():
    global available_feeds, result, length
    if request.method == 'POST':
        animal = request.form.get('animal-dropdown')
        age = request.form.get('age-dropdown')
        available_feeds = request.form.getlist('available-feeds')
        print(animal, age, available_feeds)
        result, length = calculate_feed(animal, age, available_feeds)
        print(result)
        return redirect(url_for('views.result'))

    return render_template("calculate.html", user=current_user, data=data)

@views.route('/result')
def result():
    return render_template("result.html", user=current_user, result=result, available_feeds=available_feeds, length=length)