from flask import render_template, url_for, request, redirect
from ShoppingList import app
from ShoppingList.models import List, Item, db


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        list_name = request.form['list_name']
        new_list = List(list_name=list_name)

        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your item'

    else:
        lists = List.query.order_by(List.date_created).all()
        return render_template('index.html', lists=lists)

#List functions

@app.route('/delete/<int:id>')
def delete_list(id):
    list_to_delete = List.query.get_or_404(id)
    items_to_delete = Item.query.filter(Item.list_id == id).all()

    try:
        for item in items_to_delete:
            db.session.delete(item)

        db.session.delete(list_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that list'

@app.route('/rename/<int:id>', methods=['POST', 'GET'])
def rename(id):
    list = List.query.get_or_404(id)

    if request.method == 'POST':
        list.list_name = request.form['list_name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue renaming your list'
    else:
        return render_template('rename.html', list=list)

@app.route('/<int:list_id>', methods=['POST', 'GET'])
def list(list_id):
    if request.method == 'POST':
        item_name = request.form['item_name']
        store_name = request.form['store_name']
        quantity = request.form['quantity']
        new_item = Item(item_name=item_name, store_name=store_name, quantity=quantity, list_id=list_id)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('list', list_id=list_id))
        except:
            return 'There was an issue adding your item'
    else:
        items = Item.query.order_by(Item.date_created).filter(Item.list_id == list_id).all()
        list = List.query.get_or_404(list_id)
        return render_template('list.html', items=items, list=list)
        

#Item functions

@app.route('/<int:list_id>/delete/<int:id>')
def delete(list_id, id):
    item_to_delete = Item.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('list', list_id=list_id))
    except:
        return 'There was a problem deleting that item'

@app.route('/<int:list_id>/update/<int:id>', methods=['POST', 'GET'])
def update(list_id, id):
    item = Item.query.get_or_404(id)

    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.store_name = request.form['store_name']
        item.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect(url_for('list', list_id=list_id))
        except:
            return 'There was an issue updating your item'
    else:
        list = List.query.get_or_404(list_id)
        return render_template('update.html', item=item, list=list)

@app.route('/<int:list_id>/increment/<int:id>')
def increment(list_id, id):
    item = Item.query.get_or_404(id)

    try:
        item.quantity = item.quantity + 1
        db.session.commit()
        return redirect(url_for('list', list_id=list_id))
    except:
        'There was an issue modifying your item quantity'


@app.route('/<int:list_id>/decrement/<int:id>')
def decrement(list_id, id):
    item = Item.query.get_or_404(id)

    if item.quantity - 1 == 0:
        delete(id)
    else:
        try:
            item.quantity = item.quantity - 1
            db.session.commit()
            return redirect(url_for('list', list_id=list_id))
        except:
            'There was an issue modifying your item quantity'