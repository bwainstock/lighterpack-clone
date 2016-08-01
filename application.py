from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='/'.join(['sqlite://', app.root_path, 'app.db']),
    SECRET_KEY='dev key',
    USERNAME='admin',
    PASSWORD='default'
))

db = SQLAlchemy(app)


class Item(db.Model):

    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    color  = db.Column(db.String(50))
    weight = db.Column(db.Float)
    count = db.Column(db.Integer)
    description = db.Column(db.String(50))

    def __init__(self, make, model, color, weight, count, description):
        self.make = make
        self.model = model
        self.color = color
        self.weight = weight
        self.count = count
        self.description = description

    def __repr__(self):
        return '<Item {} {}>'.format(self.make, self.model)

class ItemForm(Form):
    make = StringField('make', validators=[DataRequired()])
    model = StringField('model', validators=[DataRequired()])
    color = StringField('color', validators=[DataRequired()])
    weight = DecimalField('weight', validators=[DataRequired()])
    count = IntegerField('count', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Add')

@app.cli.command('initdb')
def initdb_command():
    db.create_all()
    print('Initialized db')

@app.route('/')
def index(errors=None):
    items = Item.query.limit(10)
    form = ItemForm()
    return render_template('index.html', errors=errors, form=form, items=items)

@app.route('/additem', methods=['POST'])
def additem():
    
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(form.make.data,
                    form.model.data,
                    form.color.data,
                    form.weight.data,
                    form.count.data,
                    form.description.data)


        db.session.add(item)
        db.session.commit()
        flash('Item added')
    
        #return "Item added"
    else:
        #return redirect(url_for('index', error=form.errors))
        flash(' '.join(form.errors))
    return redirect(url_for('index'))
