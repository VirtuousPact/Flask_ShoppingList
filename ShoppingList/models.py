from ShoppingList import db
from datetime import datetime

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(100), nullable=False)
    items = db.relationship("Item", backref='list')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<List %r>' % self.id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.id