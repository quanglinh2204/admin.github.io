from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user
from datetime import datetime
from flask import render_template
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import send_file
from wtforms.validators import DataRequired
from flask import Flask, request, jsonify
from flask import jsonify
from flask import Flask, render_template, url_for, send_from_directory
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
class Players(db.Model, UserMixin):
    __tablename__ = 'players'
    
    IdPlayer = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(255), nullable=False)
    UserPassWord = db.Column(db.String(255), nullable=False)
    FullName = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Date = db.Column(db.DateTime)
    TurnsOfPlay = db.Column(db.Integer)
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)   

def create_user(username, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = Players(UserName=username, UserPassWord=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user
def get_id(self):
        return str(self.IdPlayer)
def create_admin():
    admin_username = 'admin'
    admin_password = '12345'

  
    existing_admin = Admin.query.filter_by(username=admin_username).first()

    if not existing_admin:
       
        hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
        new_admin = Admin(username=admin_username, password=hashed_password)

        db.session.add(new_admin)
        db.session.commit()


class ListGames(db.Model):
    __tablename__ = 'list_games'
    GameId = db.Column(db.Integer, primary_key=True)
    GameName = db.Column(db.String(255))
    GameDescription = db.Column(db.Text)
    Ratio = db.Column(db.Integer)
    Poster = db.Column(db.String(255))
    Type = db.Column(db.String(255))
    Amount = db.Column(db.Integer)
    Rule = db.Column(db.String(255))
    State = db.Column(db.String(255))
    StartDay = db.Column(db.DateTime)
    LastDay = db.Column(db.DateTime)
class Gifts(db.Model):
    __tablename__ = 'gifts'
    GiftId = db.Column(db.Integer, primary_key=True)
    GiftName = db.Column(db.String(255))
    Ratio = db.Column(db.Integer)
    Amount = db.Column(db.Integer)
    State = db.Column(db.String(255))
    GameId = db.Column(db.Integer, db.ForeignKey('list_games.GameId'))
    

class PublicLinks(db.Model):
    __tablename__ = 'public_links'
    LinkId = db.Column(db.Integer, primary_key=True)
    Link = db.Column(db.String(255))
    GameId = db.Column(db.Integer)
    Poster = db.Column(db.String(255))
    Caption = db.Column(db.String(255))
class Win(db.Model):
    __tablename__ = 'win'
    WinId = db.Column(db.Integer, primary_key=True)
    IdPlayer = db.Column(db.Integer, db.ForeignKey('players.IdPlayer'))
    GiftId = db.Column(db.Integer, db.ForeignKey('gifts.GiftId'))
    Amount = db.Column(db.Integer)
    State = db.Column(db.String(255))
    player = db.relationship('Players', backref='wins', lazy=True)
    gift = db.relationship('Gifts', backref='wins', lazy=True)
class PublicLinkForm(FlaskForm):
    link = StringField('Link')
    gameId = StringField('Game Id')
    poster = StringField('Poster')
    description = StringField('Description')
    submit = SubmitField('Submit')    
class WinnerForm(FlaskForm):
    idWin = StringField('Win Id')
    idPlayer = StringField('Player Id')
    giftId = StringField('Gift Id')
    amount = StringField('Amount')
    state = StringField('State')
    submit = SubmitField('Submit')

class InputForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    gameId = StringField('Game Id', validators=[DataRequired()])
    poster = StringField('Poster', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')    
class LoginForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    gameId = StringField('Game Id', validators=[DataRequired()])
    poster = StringField('Poster', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    submit = SubmitField('Register')
@app.route('/admin', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.username == 'admin':
                return redirect(url_for('index'))
            else:
                return redirect(url_for('home'))

    return render_template('admin.html', form=form)
def index():
    return render_template('admin.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data  

        existing_user = Players.query.filter_by(UserName=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            create_user(username, password)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)
@login_manager.user_loader
def load_user(user_id):
    return Players.query.get(int(user_id))

@app.route('/admin')
def admin():
     
    if request.args.get('access') == 'granted':
        links = PublicLinks.query.all()
        return render_template('admin.html', links=links)
    else:
        return redirect(url_for('login'))
    

@app.route('/api/public_links', methods=['GET', 'POST'])
def get_or_create_public_links():
    if request.method == 'GET':
        # Handle logic to retrieve and return all public links
        return jsonify({'public_links': links_list})

    elif request.method == 'POST':
        data = request.json
        new_link = PublicLinks(Link=data['Link'], GameId=data['GameId'],
                               Poster=data['Poster'], Caption=data['Caption'], Shared=False)
        db.session.add(new_link)
        db.session.commit()
        return jsonify({'message': 'Public link created successfully'}), 201

@app.route('/api/public_links/<int:linkId>', methods=['PUT', 'DELETE'])
def edit_or_delete_link(linkId):
    if request.method == 'PUT':
        data = request.json
        updated_link = PublicLinks.query.get(linkId)
        if updated_link:
            updated_link.Link = data['Link']
            updated_link.GameId = data['GameId']
            updated_link.Poster = data['Poster']
            updated_link.Caption = data['Caption']
            db.session.commit()
            return jsonify({'message': 'Public link updated successfully'}), 200
        else:
            return jsonify({'error': 'Link not found'}), 404

    elif request.method == 'DELETE':
        link_to_delete = PublicLinks.query.get(linkId)
        if link_to_delete:
            db.session.delete(link_to_delete)
            db.session.commit()
            return jsonify({'message': 'Public link deleted successfully'}), 200
        else:
            return jsonify({'error': 'Link not found'}), 404

@app.route('/api/public_links/share/<int:linkId>', methods=['POST'])
def share_link(linkId):
    # Handle the logic for sharing the link with linkId
    # You can use request.json to get any additional data from the frontend

    return jsonify({'message': 'Link shared successfully'}), 200
        
@app.route('/winners', methods=['GET'])
def display_winners():
    winners_list = Win.query.all()
    return render_template('winners.html', winners=winners_list)
@app.route('/public-link-list', methods=['GET', 'POST'])
def public_link_list():
    form = InputForm()

    if form.validate_on_submit():
        link = form.link.data
        game_id = form.gameId.data
        poster = form.poster.data
        description = form.description.data
        new_link = PublicLinks(Link=link, GameId=game_id, Poster=poster, Caption=description)
        db.session.add(new_link)
        db.session.commit()

        
        return redirect(url_for('public_link_list'))

    links = PublicLinks.query.all()

    return render_template('admin.html', form=form, links=links)

@app.route('/winner-list')
def winner_list():
    form = WinnerForm()  # Create an instance of your form
    return render_template('winners.html', form=form)
@app.route('/input_form', methods=['GET'])
def render_input_form():
    form = InputForm()
    return render_template('admin.html', form=form)


@app.route('/input_data', methods=['POST'])
def input_data():
    form = InputForm(request.form)
    if form.validate():
      
        print(f"Link: {form.link.data}, Game Id: {form.gameId.data}, Poster: {form.poster.data}, Description: {form.description.data}")

      
        return redirect(url_for('render_input_form'))
    else:
        
        return render_template('admin.html', form=form)
@app.route('/api/add_link', methods=['POST'])
def add_link():
    data = request.json
    return jsonify({'message': 'Link added successfully'}), 201
@app.route('/copy_link/<int:link_id>', methods=['POST'])
def copy_link(link_id):
    link = PublicLinks.query.get(link_id)

    if link:
        return jsonify({'message': 'Link copied successfully', 'link_text': link.Link}), 200
    else:
        return jsonify({'message': 'Link not found'}), 404
@app.route('/winner-list', methods=['POST'])
def add_winner():
    data = request.get_json()
    player_id = data.get('playerId')
    gift_id = data.get('giftId')
    amount = data.get('amount')
    state = data.get('state')
    new_winner = Win(IdPlayer=player_id, GiftId=gift_id, Amount=amount, State=state)
    db.session.add(new_winner)
    db.session.commit()

    return jsonify({'message': 'Winner added successfully'})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)