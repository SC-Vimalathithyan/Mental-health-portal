from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Use a strong key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindcare.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MoodForm(FlaskForm):
    mood = StringField('Mood (e.g., Happy, Anxious)', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Log Mood')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/resources')
@login_required
def resources():
    # Sample resources; in production, fetch from DB or API
    resources = [
        {'title': 'Managing Anxiety', 'type': 'Article', 'link': '#'},
        {'title': 'Depression Self-Help Video', 'type': 'Video', 'link': '#'},
        {'title': 'Stress Relief Exercises', 'type': 'Exercise', 'link': '#'}
    ]
    return render_template('resources.html', resources=resources)

@app.route('/mood_tracker', methods=['GET', 'POST'])
@login_required
def mood_tracker():
    form = MoodForm()
    if form.validate_on_submit():
        entry = MoodEntry(user_id=current_user.id, date=request.form['date'], mood=form.mood.data, notes=form.notes.data)
        db.session.add(entry)
        db.session.commit()
        flash('Mood logged successfully!', 'success')
        return redirect(url_for('mood_tracker'))
    entries = MoodEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('mood_tracker.html', form=form, entries=entries)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_message = request.form['message']
        # Simulate counsellor response (replace with real API in production)
        counsellor_response = "I'm here to listen. How are you feeling today?"
        return jsonify({'response': counsellor_response})
    return render_template('chat.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)