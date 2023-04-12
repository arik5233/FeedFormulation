from flask import Blueprint, render_template , request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
from .calculate import calculate_feed
import json

nutrients_quantity_dict = json.load(open('nutrients_quantity_dict.txt'))

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    name = current_user.first_name
    users = User.query.all()
    return render_template("home.html", user=current_user, name=name, users=users)

@views.route('/calculate', methods=['GET', 'POST'])
def calculate():
    global available_feeds, result, length
    all_feeds = nutrients_quantity_dict.keys()
# 'peaking', 'layer_2', 'layer_3', 'layer_4', 'layer_5'
    if request.method == 'POST':
        animal = request.form.get('animal-dropdown')
        age = int(request.form.get('age-dropdown'))
        available_feeds = request.form.getlist('available-feeds')
        if 0 < age <= 35:
            kind = 'peaking'
        elif 35 < age <= 45:
            kind = 'layer_2'
        elif 45 < age <= 60:
            kind = 'layer_3'
        elif 60 < age <= 72:
            kind = 'layer_4'
        elif 72 < age <= 100:
            kind = 'layer_5'
        # print(animal, age, available_feeds)
        result, length = calculate_feed(kind, available_feeds)
        flash('Calculation completed Successfully!', category='success')
        return redirect(url_for('views.result'))
    if current_user.is_authenticated:
        return render_template("calculate.html", user=current_user, data=all_feeds, name=current_user.first_name)
    return render_template("calculate.html", user=current_user, data=all_feeds, name='Guest')

@views.route('/result')
def result():
    if current_user.is_authenticated:
        return render_template("result.html", user=current_user, result=result, available_feeds=available_feeds, length=length, name=current_user.first_name)
    return render_template("result.html", user=current_user, result=result, available_feeds=available_feeds, length=length)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        if request.method == 'GET':
            return render_template("updateProfile.html", user=current_user, name=current_user.first_name, obj=current_user)
        elif request.method == 'POST':
            # if post action delete is pressed, delete the user
            if request.form.get('action') == 'delete':
                db.session.delete(user)
                db.session.commit()
                flash('Profile Deleted Successfully!', category='success')
                return redirect(url_for('auth.login'))
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.contact_num = request.form.get('contact_num')
            user.address = request.form.get('address')
            db.session.commit()
            flash('Profile Updated Successfully!', category='success')
            return redirect(url_for('views.profile'))
        