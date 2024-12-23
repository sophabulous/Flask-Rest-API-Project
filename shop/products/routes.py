from flask import render_template, flash, request, redirect, url_for, flash, session, current_app
from shop import app, db, photos
from .models import Brand, Category, Product
from .forms import Addproducts
import secrets
import os

def brands():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Product,(Category.id == Product.category_id)).all()
    return categories

@app.route('/')
def home():
    products = Product.query.filter(Product.stock > 0)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories())

@app.route('/product/<int:id>')
def details_page(id):
    product = Product.query.get_or_404(id)
    return render_template('products/details_page.html', product=product, brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def brand(id):
    p_by_brand = Product.query.filter_by(brand_id=id).all()
    return render_template('products/index.html', p_by_brand=p_by_brand, brands=brands(), categories=categories())

@app.route('/category/<int:id>')
def get_category(id):
    category = Category.query.filter_by(id=id).first_or_404()
    prod_by_cat = Product.query.filter_by(category=category).all()
    return render_template('products/index.html', brands=brands(), categories=categories(), prod_by_cat=prod_by_cat)

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
def update_brand(id):
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
    return render_template('products/add_brand.html', title='Updated brand',brands='products',updatebrand=updatebrand)

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
def update_cat(id):
    # if 'email' not in session:
    #     flash('Login first please','danger')
    #     return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/add_brand.html', title='Update category',updatecat=updatecat)

@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def delete_cat(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('home'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('home'))

@app.route('/addproduct', methods=['GET','POST'])
def add_product():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == "POST" and 'image_1' in request.files:
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
            file_1 = request.files.get('image_1')
            file_2 = request.files.get('image_2')
            file_3 = request.files.get('image_3')

            image_1 = photos.save(file_1, name=secrets.token_hex(10) + ".")

            # Validate and save image_2 (optional)
            if file_2 and photos.file_allowed(file_2, file_2.filename):
                image_2 = photos.save(file_2, name=secrets.token_hex(10) + ".")
            else:
                image_2 = None  # Default to None if no file is uploaded

            # Validate and save image_3 (optional)
            if file_3 and photos.file_allowed(file_3, file_3.filename):
                image_3 = photos.save(file_3, name=secrets.token_hex(10) + ".")
            else:
                image_3 = None  # Default to None if no file is uploaded

        except Exception as e:
            flash(f"Error saving files: {str(e)}", "danger")
            return redirect(url_for('add_product'))

        product = Product(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,
                             category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(product)
        flash(f'The product {name} was added in the database', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    # Debug: Print form errors if validation fails
    if request.method == "POST" and not form.validate():
        print(form.errors)
    return render_template('products/add_product.html', form=form, title='Add a Product', brands=brands,
                           categories=categories)
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('home'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('home'))