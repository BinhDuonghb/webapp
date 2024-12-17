from coffe import db, bcrypt,login_manager
from flask_login import UserMixin
from datetime import datetime

import base64
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False,unique=True)
    password = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    budget = db.Column(db.Float(),nullable = False, default=1000)
    img = db.relationship('Image',backref='user_image',lazy=True)
    items = db.relationship('Item',backref="owned_user",lazy = True)
    history = db.relationship("History", backref='user_history', lazy=True)
    def __repr__(self) -> str:
        return f"User: {self.name}"
    
    @property
    def set_password(self):
        return self.password
    @set_password.setter
    def set_password(self,bare_password):
        self.password = bcrypt.generate_password_hash(bare_password).decode("utf-8")
    def password_check(self,input_password):
        return bcrypt.check_password_hash(self.password,input_password)
    @property
    def budget_display(self):
        str_budget = str(self.budget)
        int_part, dec_part = str_budget.split('.') if '.' in str_budget else (str_budget, "")

        output = []
        count = 0
        for i in range(len(int_part) - 1, -1, -1):
            output.insert(0, int_part[i])
            count += 1
            if count % 3 == 0 and i != 0:
                output.insert(0, ',')

        if dec_part:
            output.append('.')
            dec_part = dec_part.rstrip('0')[:2] 
            output.append(dec_part)

        return ''.join(output)
    
    def affordable(self,item_price):
        return self.budget >= item_price 
    
    def history(self,activity,activity_type,cost):
        new_history = History(user_id=self.id, activity=activity, date=datetime.now(),activity_type=activity_type,cost = cost)
        db.session.add(new_history)
        db.session.commit()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    onSale = db.Column(db.Boolean(),default=False)
    description = db.Column(db.String(),nullable=False)
    img = db.relationship('ItemImage',backref='item_image',lazy=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def set_owner(self,user_id):
        self.owner = user_id
        db.session.commit()
    def __repr__(self) -> str:
        return f"Item: {self.name}"
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    activity_type = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float())
    def formatTime(self):
        return self.date.strftime('%Y-%m-%d %H:%M')
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False) 
    def set_image(self,img,mimetype,name):
        self.img = img
        self.mimetype = mimetype
        self.name = name
        db.session.commit()
    def b64img(self):
        return base64.b64encode(self.img).decode("utf-8")
class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    item_id = db.Column(db.Integer(),db.ForeignKey('item.id'),nullable=False) 
    def b64img(self):
        return base64.b64encode(self.img).decode("utf-8")
    def __repr__(self) -> str:
        return f"Image: {self.name}"
    