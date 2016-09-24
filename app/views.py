from flask import Flask, render_template, request, url_for, redirect, \
				flash, session
import os
from flask_sqlalchemy import SQLAlchemy



from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'




from forms import *

from models import *
from emails import send_mail
from decorators import check_confirmed


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',form=form)

   


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate():
		username =  form.username.data
		password = form.password.data
		user_exist = User.query.filter_by(username=username).first()
		if user_exist is not None and bcrypt.check_password_hash(user_exist.password,\
		 		password) == True:
			login_user(user_exist,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('registration')) 
		
		flash('invalid login details')
	return render_template('index.html',form=form)




@app.route('/registration', methods = ['GET','POST'])
def registration():
	form = RegistrationForm()
	if request.method == 'POST': 
		if form.validate():
			email = form.email.data
			username = form.username.data
			password = form.password.data
			user = User(username=username,
						email=email,password=password,confirmed=False)

			db.session.add(user)
			db.session.commit()
			token =  user.generate_confirmation_token()
			confirm_url = url_for('confirm_email',token=token,_external=True)
			html = render_template('email/email.html',user=user,confirm_url=confirm_url)
			subject = "confirm your account"
			send_mail(user.email,subject,html)

			return redirect(url_for('unconfirmed'))
		flash('username or email already exist')
	return render_template('registration.html',form=form)

@app.route('/home')
@login_required
@check_confirmed
def home():
	return render_template('home.html')


@app.route('/profile', methods = ['GET','POST'])
def profile():
	form = ProfileForm()
	form.school.choices = [('ABU Zaria', 'ABU Zaria'),
						 ('University of', 'Python'), ('text', 'Plain Text')]
	form.gender.choices = [('male','Male'),('female','Female')]
	if request.method == 'POST':
		if form.validate():
			return redirect(url_for('registration'))
		return 'bad form'
	return render_template('profile.html',form=form)


@app.route('/confirm_email/<token>')
@login_required
def confirm_email(token):
	if current_user.confirmed:
		return 'you have been confirmed'
	if current_user.confirm(token):
		return 'thank you for confirmation'
	else:
		return 'bad token'


@app.route('/unconfirmed')
@login_required
def unconfirmed():
	if current_user.confirmed:
		return redirect(url_for('home'))
	return render_template('unconfirmed.html')


@app.route('/resend')
@login_required
def resend():
	token = current_user.generate_confirmation_token()
	confirm_url = url_for('confirm_email',token=token,_external=True)
	html = render_template('email/email.html',user=current_user,confirm_url=confirm_url)
	subject = "confirm your account"
	send_mail(current_user.email,subject,html)
	flash('another link has been sent','success')
	flash(current_user.email)
	return redirect(url_for('unconfirmed'))

