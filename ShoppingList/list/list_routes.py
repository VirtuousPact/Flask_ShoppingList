from flask import Blueprint, redirect, url_for, render_template
from flask import current_app as app
from .models import Item, db
from ShoppingList.home.models import List
from .forms import ItemForm

# Blueprint Configuration
list_bp = Blueprint(
    'list_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@list_bp.route('/<int:list_id>', methods=['POST', 'GET'])
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
            return redirect(url_for('list_bp.list', list_id=list_id))
        except:
            return 'There was an issue adding your item'
    else:
        items = Item.query.order_by(Item.date_created).filter(Item.list_id == list_id).all()
        list = List.query.get_or_404(list_id)
        return render_template('list.html', items=items, list=list, form=form)

@list_bp.route('/<int:list_id>/delete/<int:id>')
def delete(list_id, id):
    item_to_delete = Item.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('list_bp.list', list_id=list_id))
    except:
        return 'There was a problem deleting that item'

@list_bp.route('/<int:list_id>/update/<int:id>', methods=['POST', 'GET'])
def update(list_id, id):
    item = Item.query.get_or_404(id)
    form = ItemForm()
    if form.validate_on_submit():
        item.item_name = form.name.data
        item.store_name = form.store_name.data
        item.quantity = form.quantity.data

        try:
            db.session.commit()
            return redirect(url_for('list_bp.list', list_id=list_id))
        except:
            return 'There was an issue updating your item'
    else:
        list = List.query.get_or_404(list_id)
        form.name.data = item.item_name
        form.store_name.data = item.store_name
        form.quantity.data = item.quantity
        return render_template('update.html', item=item, list=list, form=form)

@list_bp.route('/<int:list_id>/increment/<int:id>')
def increment(list_id, id):
    item = Item.query.get_or_404(id)

    try:
        item.quantity = item.quantity + 1
        db.session.commit()
        return redirect(url_for('list_bp.list', list_id=list_id))
    except:
        'There was an issue modifying your item quantity'


@list_bp.route('/<int:list_id>/decrement/<int:id>')
def decrement(list_id, id):
    item = Item.query.get_or_404(id)

    if item.quantity - 1 == 0:
        return redirect(url_for('list_bp.list', list_id=list_id))
    else:
        try:
            item.quantity = item.quantity - 1
            db.session.commit()
            return redirect(url_for('list_bp.list', list_id=list_id))
        except:
            'There was an issue modifying your item quantity'