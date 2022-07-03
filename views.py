from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import Post, User, Like, About, Project, Contact, Visit
from . import db
import socket
from datetime import datetime


app = Flask(__name__)

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home_page():

    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = "home-page"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends


    posts = Post.query.order_by(-Post.id).limit(7).all()
    projects = Project.query.order_by(-Project.id).limit(3).all()
    return render_template('index.html', posts=posts, projects=projects, user=current_user)

@views.route('/writing')
def writing_page():

    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = "writing"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends

    posts = Post.query.all()
    return render_template('writing.html', posts=posts, user=current_user)

@views.route('/about-me')
def aboutme_page():

    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = "about-me"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends

    abouts = About.query.filter_by(id='1').first()
    return render_template('about-me.html', abouts=abouts, user=current_user)

@views.route('/timeline')
def timeline_page():

    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = "timeline"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends


    return render_template('timeline.html', user=current_user)

@views.route('/admin/update-post/<id>', methods=['GET', 'POST'])
@login_required
def updatepost_page(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == "POST":
        title_edit = request.form.get('title_edit')
        edit = request.form.get('edit')
        found_text = Post.query.filter_by(id = id). first()
        found_text.title = title_edit
        found_text.text = edit
        db.session.commit()
        flash('Post updated', category='success')
        return redirect(url_for('views.adminposts_page', user=current_user, post=post))

    return render_template('Admin/update-post.html', post=post, user=current_user)


@views.route('/writing-detail/<id>', methods=['GET'])
def writingdetail_page(id):


    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = f"writing-detail-{id}"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends


    post = Post.query.filter_by(id=id).first()
    return render_template('writing-detail.html', post=post, user=current_user)

@views.route('/contact-me', methods=['GET', 'POST'])
def contact_page():

    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = "contact-page"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends


    if request.method == "POST":
        name = request.form.get('name')
        mail = request.form.get('mail')
        message = request.form.get('message')
        IPAddr = socket.gethostbyname(socket.gethostname())
        statu = 0

        if not name:
            flash('please, fill the name field.', category='error')
        elif not mail:
            flash('please, fill the mail field.', category='error')
        elif not message:
            flash('please, fill the message field.', category='error')
        else:
            contact = Contact(name=name, mail=mail, message=message, statu=statu, ipaddress=IPAddr)
            db.session.add(contact)
            db.session.commit()
            flash('I got your message, I am going to answer you via email.', category='success')
            return redirect(url_for('views.contact_page'))
    return render_template('contact.html', user=current_user)


@views.route("/admin/admin-home")
@views.route("/admin/home")
@login_required
def adminhome_page():
    posts = Post.query.all()
    projects = Project.query.all()
    contacts = Contact.query.all()
    about = About.query.filter_by(id='1').first()

    return render_template('Admin/admin-home.html', user=current_user, posts=posts, about=about, projects=projects, contacts=contacts)

@views.route("/admin/posts", methods=['GET', 'POST'])
@login_required
def adminposts_page():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')

        text_exists = Post.query.filter_by(text=text).first()
        title_exists = Post.query.filter_by(title=title).first()

        if text_exists or title_exists:
            flash('This text or title is already exist!', category='error')

        elif not text:
            flash('Text area cannot be empth here!', category='error')
        
        elif not title:
            flash('Title area cannot be empth here!', category='error')
        
        else:
            post = Post(text=text, title=title, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post published!', category='success')

    posts = Post.query.all()
    return render_template('Admin/Posts.html', user=current_user, posts=posts)

@views.route("/admin/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('Post does not exist.', category='error')
    
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfuly.', category='success')
    
    return redirect(url_for('views.adminposts_page'))

@views.route("/admin/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):

    IPAddr = socket.gethostbyname(socket.gethostname())

    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(ipaddress=IPAddr, post_id=post_id).first()

    if not post:
        flash('Post does not exist!', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(ipaddress=IPAddr, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return redirect(url_for('views.adminposts_page'))

@views.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like_post(post_id):

    IPAddr = socket.gethostbyname(socket.gethostname())

    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(ipaddress=IPAddr, post_id=post_id).first()

    if not post:
        flash('Post does not exist!', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(ipaddress=IPAddr, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return redirect(url_for('views.writingdetail_page', id=post_id))

@views.route('/admin/admin-about', methods=['POST', 'GET'])
@login_required
def adminabout_page():
    about = About.query.filter_by(id='1').first()

    if request.method == "POST":
        header = request.form.get('header')
        body = request.form.get('body')
        profil_photo = request.form.get('profil_photo')
        p1 = request.form.get('p1')
        p1_link = request.form.get('p1_link')
        p2= request.form.get('p2')
        p2_link = request.form.get('p2_link')
        p3 = request.form.get('p3')
        p3_link = request.form.get('p3_link')
        p4 = request.form.get('p4')
        p4_link = request.form.get('p4_link')
        p5 = request.form.get('p5')
        p5_link = request.form.get('p5_link')
        date_created = datetime.now()
        random_facts = request.form.get('random_facts')

        found_about = About.query.filter_by(id = '1').first()
        found_about.header = header
        found_about.body = body
        found_about.profil_photo = profil_photo
        found_about.p1 = p1
        found_about.p1_link = p1_link
        found_about.p2 = p2
        found_about.p2_link = p2_link
        found_about.p3 = p3
        found_about.p3_link = p3_link
        found_about.p4 = p4
        found_about.p4_link = p4_link
        found_about.p5 = p5
        found_about.p5_link = p5_link
        found_about.date_created = date_created
        found_about.random_facts = random_facts
        db.session.commit()
        flash('About page updated.', category='success')
        return redirect(url_for('views.adminabout_page'))
    
    return render_template("admin/admin-about.html", user=current_user, about=about)


@views.route('/admin/admin-project', methods=['POST', 'GET'])
@login_required
def project():
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        photo = request.files.get('photo')
        status = request.form.get('status')
        
        name_exists = Project.query.filter_by(name=name).first()
        description_exists = Project.query.filter_by(description=description).first()

        if name_exists or description_exists:
            flash('This text or title is already exist!', category='error')

        elif not name or not description or not photo or not status:
            flash('some places are empty, fill it.', category='error')
        
        else:
            project = Project(name=name, description=description, photo=photo, status=status)
            db.session.add(project)
            db.session.commit()
            flash('Project is succesfully added.', category='success')

    projects = Project.query.all()
    return render_template('admin/admin-project.html', user=current_user, projects=projects)


@views.route("/admin/delete-project/<id>")
@login_required
def delete_project(id):
    project = Project.query.filter_by(id=id).first()

    if not project:
        flash('Post does not exist.', category='error')
    
    else:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfuly.', category='success')
    
    return redirect(url_for('views.project'))

@views.route('/admin/admin-contact')
@login_required
def admincontact():
    messages = Contact.query.all()
    return render_template('admin/admin-contact.html', user=current_user, messages=messages)

@views.route("/admin/admin-project-edit/<id>", methods=['POST', 'GET'])
@login_required
def adminprojectedit(id):
    projects = Project.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        photo = request.form.get('photo')
        status = request.form.get('status')

        found_project = Project.query.filter_by(id=id).first()
        found_project.name = name
        found_project.description = description
        found_project.photo = photo
        found_project.status = status
        db.session.commit()
        flash('project is changed.', category='success')
        return redirect(url_for('views.project'))

    return render_template('admin/admin-project-edit.html', user=current_user, projects=projects)
