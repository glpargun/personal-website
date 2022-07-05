from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from . import db
from .models import User, About, Post, Project,Contact
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/Login", methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.adminhome_page"))

            else:
                flash('password is incorrect.', category="error")
        else:
            flash('your username does not exist.', category="error")
    return render_template('Admin/login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succesfully logout. If you like, you can use the arrow to go to homepage.", category='success')
    return redirect(url_for("auth.sign_in"))




@auth.route("/create")
def sign_up():
    username = 'glpargun'
    password = 'Hayat+3537'
    name = 'Galip'
    surname= 'Argun'
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'), name=name, surname=surname)
    db.session.add(new_user)
    db.session.commit()

    return 'created'


@auth.route("/about")
def about():
    header = 'glpargun'
    body = 'Hayat+3537'
    profil_photo = 'Galip'
    p1= 'Argun'
    p2= 'Argun'
    p3= 'Argun'
    p4= 'Argun'
    p5= 'Argun'
    random_facts = 'Argun'
    new_user = About(header=header, body=body, profil_photo=profil_photo, p1=p1, p2=p2, p3=p3, p4=p4, p5=p5, random_facts=random_facts)
    db.session.add(new_user)
    db.session.commit()

    return 'created'

