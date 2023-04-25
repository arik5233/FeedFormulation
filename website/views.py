from flask import Blueprint, render_template , request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
from .calculate import calculate_feed
import json

nutrients_quantity_dict = {}
nutrients_quantity_dict['hen'] = json.load(open('nutrients_quantity_dict.txt'))

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    name = current_user.first_name
    users = User.query.all()
    return render_template("home.html", user=current_user, name=name, users=users)

@views.route('/calculate', methods=['GET', 'POST'])
def calculate():
    global available_feeds, result, length, prices, animal
    
# 'peaking', 'layer_2', 'layer_3', 'layer_4', 'layer_5'
    if request.method == 'POST':
        try:
            age = int(request.form.get('age-dropdown'))
            available_feeds = request.form.getlist('available-feeds')
            animal = request.form.get('animal-dropdown')
            prices = [float(x) for x in request.form.getlist('price_container') if x != '']
            if len(available_feeds) == 0:
                flash('Please select at least one feed!', category='error')
                return redirect(url_for('views.calculate'))
            if animal == None:
                flash('Please select an animal first!', category='error')
                return redirect(url_for('views.calculate'))
            if len(prices) != len(available_feeds):
                if len(prices) < len(available_feeds):
                    flash('Please enter price for all the feeds!', category='error')
                    return redirect(url_for('views.calculate'))
                else:
                    flash('Feed not selected for given price!', category='error')
                    return redirect(url_for('views.calculate'))
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
            
            result, length = calculate_feed(kind, available_feeds)
            
            print(available_feeds, prices)
            flash('Calculation completed Successfully!', category='success')
            return redirect(url_for('views.result'))
        except TypeError:
            flash('Please enter a valid age!', category='error')
        except UnboundLocalError:
            flash('Please select an animal!', category='error')
    all_feeds = nutrients_quantity_dict['hen'].keys()

    if current_user.is_authenticated:
        return render_template("calculate.html", user=current_user, data=all_feeds, name=current_user.first_name)
    return render_template("calculate.html", user=current_user, data=all_feeds, name='Guest')

@views.route('/result')
def result():
    costs = []
    # print(available_feeds, prices, result, length)
    for x in range(len(available_feeds)):
        costs.append(round((result[x]/100) * prices[x], 2))


    if current_user.is_authenticated:
        return render_template("result.html", user=current_user, result=result, available_feeds=available_feeds, length=length, prices=prices, costs=costs, total_cost=sum(costs), name=current_user.first_name)
    return render_template("result.html", user=current_user, result=result, available_feeds=available_feeds, length=length, prices=prices, costs=costs, total_cost=sum(costs))

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

@views.route('/vet/<int:id>', methods=['GET', 'POST'])
@login_required
def user_profile(id):
    user = User.query.filter_by(id=id).first()
    if user==current_user:
        return redirect(url_for('views.profile'))
    # if method is post, then retrieve the rating
    if request.method == 'POST':
        rating = request.form.get('rate')
        # add rating to the user
        user.rating = int(rating)
        db.session.commit()
        flash('Review Submitted Successfully!', category='success')
        return render_template("wall_norating.html", user=current_user, name=current_user.first_name, obj=user)
        # return redirect(url_for('views.user_profile', user=current_user, name=current_user.first_name, obj=user))

        
    return render_template("wall.html", user=current_user, name=current_user.first_name, obj=user)