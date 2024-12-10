from flask import render_template, flash, request, redirect, url_for, flash, session
from shop import db, app, photos
from .models import Brand, Category, Product
from .forms import Addproducts
import secrets

def brands():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Product,(Category.id == Product.category_id)).all()
    return categories

@app.route('/addbrand', methods=['GET', 'POST'])
def add_brand():
    if request.method == "POST":
        get_brand = request.form.get('brand')
        brand = Brand(name=get_brand)
        db.session.add(brand)
        flash(f'The brand {get_brand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('add_brand'))

    return render_template('products/add_brand.html', brands="products")

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    # if 'email' not in session:
    #     flash('Login first please','danger')
    #     return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('products'))
    brand = updatebrand.name
    return render_template('products/addbrand.html', title='Updated brand',brands='products',updatebrand=updatebrand)

@app.route('/addcat', methods=['GET', 'POST'])
def add_cat():
    if request.method == "POST":
        get_cat = request.form.get('category')
        cat = Category(name=get_cat)
        db.session.add(cat)
        flash(f'The category {get_cat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('add_cat'))

    return render_template('products/add_brand.html')

@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    # if 'email' not in session:
    #     flash('Login first please','danger')
    #     return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Update category',updatecat=updatecat)

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == "POST" and 'image' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        # Debug: Check files, brand, and category
        print(request.files)
        try:
            image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        except Exception as e:
            flash(f'photo was not saved!', 'failure')
            return redirect(url_for('addproduct'))
        product = Product(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,
                             category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(product)
        flash(f'The product {name} was added in the database', 'success')
        db.session.commit()
        return redirect(url_for('add_brand'))
    # Debug: Print form errors if validation fails
    if request.method == "POST" and not form.validate():
        print(form.errors)
    return render_template('products/add_product.html', form=form, title='Add a Product', brands=brands,
                           categories=categories)