from flask import Blueprint, render_template, url_for, redirect
from flask import current_app as app
from .models import List, db
from ShoppingList.list.models import Item
from .forms import ListForm

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=['POST', 'GET'])
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

@home_bp.route('/delete/<int:id>')
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

@home_bp.route('/rename/<int:id>', methods=['POST', 'GET'])
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


        
