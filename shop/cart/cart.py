from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import db, app
from shop.products.models import Product
from shop.products.routes import brands, categories
import json


def merge_dicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addtocart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Product.query.filter_by(id=product_id).first()

        if request.method == "POST":
            item_dict = {
                product_id: {
                    'name': product.name,
                    'price': float(product.price),
                    'discount': product.discount,
                    'quantity': quantity,
                    'image': product.image_1,
                    'colors': product.colors
                }
            }
            if 'shopping_cart' in session:
                print(session['shopping_cart'])
                if product_id in session['shopping_cart']:
                    for key, item in session['shopping_cart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['shopping_cart'] = merge_dicts(session['shopping_cart'], item_dict)
                    return redirect(request.referrer)
            else:
                session['shopping_cart'] = item_dict
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/cart')
def cart():
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grand_total = 0
    for key, product in session['shopping_cart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        grand_total = float("%.2f" % (1.06 * subtotal))
    tax = ("%.2f" %(.06 * float(subtotal)))
    return render_template('products/cart.html', tax=tax, grand_total=grand_total, brands=brands(),
                           categories=categories())


@app.route('/updatecart/<int:code>', methods=['POST'])
def update_cart(code):
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['shopping_cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart'))


@app.route('/deleteitem/<int:id>')
def delete_item(id):
    if 'shopping_cart' not in session or len(session['shopping_cart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['shopping_cart'].items():
            if int(key) == id:
                session['shopping_cart'].pop(key, None)
                return redirect(url_for('cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))


@app.route('/clearcart')
def clear_cart():
    try:
        session.pop('shopping_cart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)