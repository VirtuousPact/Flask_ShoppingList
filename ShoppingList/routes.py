from flask import render_template, url_for, request, redirect, flash
from ShoppingList import app
from ShoppingList.models import List, Item, db
from .forms import ListForm, ItemForm


@app.route('/', methods=['POST', 'GET'])
def index():
    form = ListForm()
    if form.validate_on_submit():
        list_name = form.name.data
        new_list = List(list_name=list_name)

        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your item'
    lists = List.query.order_by(List.date_created).all()
    return render_template('index.html', form=form, lists=lists)

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
    form = ListForm()
    if form.validate_on_submit():
        list.list_name = form.name.data
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue renaming your list'
    else:
        form.name.data = list.list_name
        return render_template('rename.html', form=form, list=list)

@app.route('/<int:list_id>', methods=['POST', 'GET'])
def list(list_id):
    form = ItemForm()
    if form.validate_on_submit():
        item_name = form.name.data
        store_name = form.store_name.data
        quantity = form.quantity.data
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
        return render_template('list.html', items=items, list=list, form=form)
        

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
    form = ItemForm()
    if form.validate_on_submit():
        item.item_name = form.name.data
        item.store_name = form.store_name.data
        item.quantity = form.quantity.data

        try:
            db.session.commit()
            return redirect(url_for('list', list_id=list_id))
        except:
            return 'There was an issue updating your item'
    else:
        list = List.query.get_or_404(list_id)
        form.name.data = item.item_name
        form.store_name.data = item.store_name
        form.quantity.data = item.quantity
        return render_template('update.html', item=item, list=list, form=form)

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
        return redirect(url_for('list', list_id=list_id))
    else:
        try:
            item.quantity = item.quantity - 1
            db.session.commit()
            return redirect(url_for('list', list_id=list_id))
        except:
            'There was an issue modifying your item quantity'