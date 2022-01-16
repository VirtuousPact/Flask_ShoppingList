from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item_name = request.form['item_name']
        store_name = request.form['store_name']
        quantity = request.form['quantity']
        new_item = Item(item_name=item_name, store_name=store_name, quantity=quantity)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your item'

    else:
        items = Item.query.order_by(Item.date_created).all()
        return render_template('index.html', items=items)

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Item.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that item'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    item = Item.query.get_or_404(id)

    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.store_name = request.form['store_name']
        item.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your item'
    
    else:
        return render_template('update.html', item=item)

@app.route('/increment/<int:id>')
def increment(id):
    item = Item.query.get_or_404(id)

    try:
        item.quantity = item.quantity + 1
        db.session.commit()
        return redirect('/')
    except:
        'There was an issue modifying your item quantity'


@app.route('/decrement/<int:id>')
def decrement(id):
    item = Item.query.get_or_404(id)

    if item.quantity - 1 == 0:
        delete(id)
    else:
        try:
            item.quantity = item.quantity - 1
            db.session.commit()
            return redirect('/')
        except:
            'There was an issue modifying your item quantity'

if __name__ == "__main__":
    app.run(debug=True)