from flask import Blueprint, render_template, request, flash, redirect, url_for,Response, Flask
from flask_login import login_required, current_user
from sqlalchemy import func
from .models import Post, User, Like, About, Project, Contact, Visit, Upload
from . import db
import socket
from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename
import os
import uuid as uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/image/Upload/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

    like = Like(ipaddress=IPAddr, post_id=id)
    db.session.add(like)
    db.session.commit()

    post = Post.query.get_or_404(id)
    read = Like.query.filter_by(post_id=id).count()
    return render_template('writing-detail.html', post=post, read=read, user=current_user)


@views.route('/about-me')
def aboutme_page():
    id=1
    # ip adress kayıt starts

    IPAddr = socket.gethostbyname(socket.gethostname())
    visit = datetime.now()
    page = "about-me"
    visit = Visit(ipaddress=IPAddr, visit=visit, page=page)
    db.session.add(visit)
    db.session.commit()

    # ip adress kayıt ends

    abouts = About.query.get_or_404(id)
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

@views.route('/Admin/update-post/<id>', methods=['GET', 'POST'])
@login_required
def updatepost_page(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == "POST":
        title_edit = request.form.get('title_edit')
        edit = request.form.get('edit')
        kapak_photo = request.files.get('kapak_photo')
        kapak_photo_text = request.form.get('kapak_photo_text')

        if request.files['kapak_photo'].filename == '':
            found_text = Post.query.filter_by(id = id). first()
            found_text.title = title_edit
            found_text.text = edit
            found_text.kapak_photo = kapak_photo_text
            db.session.commit()
            flash('Post updated', category='success')
            return redirect(url_for('views.adminposts_page', user=current_user, post=post))
            
        else:
            filename=secure_filename(kapak_photo.filename)
            photo_name = str(uuid.uuid1()) + "_" + filename
            kapak_photo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],photo_name))
            found_text = Post.query.filter_by(id = id). first()
            found_text.title = title_edit
            found_text.text = edit
            found_text.kapak_photo = photo_name
            upload = Upload(photo=photo_name, kategori='2')
            db.session.add(upload)
            db.session.commit()
            flash('Post updated', category='success')
            return redirect(url_for('views.adminposts_page', user=current_user, post=post))


    return render_template('/Admin/update-post.html', post=post, user=current_user)


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

@views.route("/admin/")
def directadmin():
    return redirect(url_for("views.adminhome_page"))

@views.route("/admin/admin-home")
@views.route("/admin/home")
@login_required
def adminhome_page():
    posts = Post.query.order_by(-Post.id).limit(15).all()
    projects = Project.query.all()
    contacts = Contact.query.all()
    about = About.query.filter_by(id='1').first()
    index_total_visit = Visit.query.filter_by(page='home-page').count()
    
    # index data
    index_one_month_visit = Visit.query.filter(Visit.page=='home-page').filter(Visit.visit > date.today() - timedelta(days=30)).count()
    index_one_week_visit = Visit.query.filter(Visit.page=='home-page').filter(Visit.visit > date.today() - timedelta(days=7)).count()
    index_one_day_visit = Visit.query.filter(Visit.page=='home-page').filter(Visit.visit > date.today() - timedelta(days=1)).count()

    # about-me data
    about_me_one_week_visit = Visit.query.filter(Visit.page=='about-me').filter(Visit.visit > date.today() - timedelta(days=7)).count()
    about_me_one_day_visit = Visit.query.filter(Visit.page=='about-me').filter(Visit.visit > date.today() - timedelta(days=1)).count()

    # timeline data
    timeline_one_month_visit = Visit.query.filter(Visit.page=='timeline').filter(Visit.visit > date.today() - timedelta(days=30)).count()
    timeline_one_week_visit = Visit.query.filter(Visit.page=='timeline').filter(Visit.visit > date.today() - timedelta(days=7)).count()
    timeline_one_day_visit = Visit.query.filter(Visit.page=='timeline').filter(Visit.visit > date.today() - timedelta(days=1)).count()

    # contact-me data
    contact_one_month_visit = Visit.query.filter(Visit.page=='contact-page').filter(Visit.visit > date.today() - timedelta(days=30)).count()
    contact_one_week_visit = Visit.query.filter(Visit.page=='contact-page').filter(Visit.visit > date.today() - timedelta(days=7)).count()
    contact_one_day_visit = Visit.query.filter(Visit.page=='contact-page').filter(Visit.visit > date.today() - timedelta(days=1)).count()


    like = Like.query.all()

    return render_template('Admin/admin-home.html', index_one_day_visit=index_one_day_visit, index_one_week_visit=index_one_week_visit, index_total_visit=index_total_visit, 
    about_me_one_week_visit=about_me_one_week_visit, about_me_one_day_visit=about_me_one_day_visit, 
    index_one_month_visit=index_one_month_visit, like=like,
    contact_one_month_visit = contact_one_month_visit, contact_one_day_visit=contact_one_day_visit, contact_one_week_visit=contact_one_week_visit,
    timeline_one_month_visit = timeline_one_month_visit, timeline_one_week_visit=timeline_one_week_visit, timeline_one_day_visit=timeline_one_day_visit,
    user=current_user, posts=posts, about=about, projects=projects, contacts=contacts)

@views.route("/admin/posts", methods=['GET', 'POST'])
@login_required
def adminposts_page():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')
        kapak_photo = request.files.get('kapak_photo')

        text_exists = Post.query.filter_by(text=text).first()
        title_exists = Post.query.filter_by(title=title).first()

        if text_exists or title_exists:
            flash('This text or title is already exist!', category='error')

        elif not text:
            flash('Text area cannot be empth here!', category='error')
        
        elif not title:
            flash('Title area cannot be empth here!', category='error')
        
        else:
            filename=secure_filename(kapak_photo.filename)
            photo_name = str(uuid.uuid1()) + "_" + filename
            kapak_photo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],photo_name))
            post = Post(text=text, title=title, author = current_user.id, kapak_photo=photo_name)
            upload = Upload(photo=photo_name, kategori='2')
            db.session.add(post)
            db.session.add(upload)
            db.session.commit()
            flash('Post published!', category='success')

    posts = Post.query.all()
    return render_template('/Admin/Posts.html', user=current_user, posts=posts)

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

@views.route("admin/admin-about", methods=['POST', 'GET'])
@login_required
def adminabout_page():
    about = About.query.filter_by(id=1).first()
    uploads = Upload.query.order_by(-Upload.id).all()

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
    
    return render_template("/Admin/admin-about.html", user=current_user, uploads=uploads, about=about)


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

        elif not name or not description or not status:
            flash('some places are empty, fill it.', category='error')
        
        elif not photo:
            flash('photo does not exists.', category='error')
        
        else:
            filename=secure_filename(photo.filename)
            photo_name = str(uuid.uuid1()) + "_" + filename
            photo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],photo_name))
            project = Project(name=name, description=description, photo=photo_name, status=status)
            db.session.add(project)
            db.session.commit()
            flash('Project is succesfully added.', category='success')

    projects = Project.query.all()
    return render_template('/Admin/admin-project.html', user=current_user, projects=projects)


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
    return render_template('/Admin/admin-contact.html', user=current_user, messages=messages)

@views.route("/admin/admin-project-edit/<id>", methods=['POST', 'GET'])
@login_required
def adminprojectedit(id):
    projects = Project.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        photo_text = request.form.get('photo_text')
        photo = request.files.get('photo')
        status = request.form.get('status')

        if request.files['photo'].filename == '':
            found_project = Project.query.filter_by(id=id).first()
            found_project.name = name
            found_project.description = description
            found_project.photo = photo_text
            found_project.status = status
            db.session.commit()
            flash('project is changed.', category='success')
            return redirect(url_for('views.project'))
        
        else:
            filename=secure_filename(photo.filename)
            photo_name = str(uuid.uuid1()) + "_" + filename
            photo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],photo_name))
            found_project = Project.query.filter_by(id=id).first()
            found_project.name = name
            found_project.description = description
            found_project.photo = photo_name
            found_project.status = status
            upload = Upload(photo=photo_name, kategori='3')
            db.session.add(upload)
            db.session.commit()
            flash('Project updated', category='success')
            return redirect(url_for('views.project'))



        

    return render_template('/Admin/admin-project-edit.html', user=current_user, projects=projects)

@views.route("/admin/admin-upload", methods=['POST', 'GET'])
@login_required
def adminupload():
    uploads = Upload.query.all()
    if request.method == 'POST':
        photo = request.files.get('photo')
        kategori = request.form.get('kategori')

        if not photo:
            flash('choose a file', category='error')
            
        else:           
            filename=secure_filename(photo.filename)
            photo_name = str(uuid.uuid1()) + "_" + filename
            photo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],photo_name))
            upload = Upload(photo=photo_name, kategori=kategori)
            db.session.add(upload)
            db.session.commit()
            flash("Uploaded!", category='success')
            return redirect(url_for("views.adminupload"))

    return render_template('/Admin/admin-upload.html', user=current_user, uploads=uploads)

@views.route("/admin/admin-upload-delete/<id>", methods=['POST', 'GET'])
@login_required
def adminuploaddelete(id):
    upload = Upload.query.filter_by(id=id).first()

    if not project:
        flash('Upload does not exist.', category='error')
    
    else:
        db.session.delete(upload)
        db.session.commit()
        flash('Upload deleted successfuly.', category='success')
    
    return redirect(url_for('views.adminupload'))