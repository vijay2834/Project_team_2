# routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes import execute_query, fetch_all, fetch_one, verify_password
import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin authentication middleware
@admin.before_request
def check_admin():
    # Skip authentication check for login route
    if request.endpoint == 'admin.login':
        return None
    
    # Ensure only admins can access admin routes
    if 'logged_in' not in session or session.get('role_id') != 1:
        flash('You do not have permission to access the admin area.', 'danger')
        return redirect(url_for('admin.login'))

@admin.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in as admin, redirect to dashboard
    if 'logged_in' in session and session.get('role_id') == 1:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not email or not password:
            flash('Please enter both email and password', 'danger')
            return render_template('admin/login.html')
        
        try:
            # Check if user exists and is an admin
            query = """
            SELECT * FROM USER
            WHERE Email = %s AND RoleID = 1
            """
            admin_user = fetch_one(query, (email,))
            
            if admin_user and verify_password(admin_user['Password'], password):
                # Set session data
                session['logged_in'] = True
                session['user_id'] = admin_user['UserID']
                session['user_name'] = f"{admin_user['FirstName']} {admin_user['LastName']}"
                session['role_id'] = admin_user['RoleID']
                
                flash('Welcome to the admin dashboard!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid credentials or insufficient permissions', 'danger')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
            
    return render_template('admin/login.html')

@admin.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('admin.login'))

@admin.route('/')
def dashboard():
    try:
        # Count total pets
        pet_count_query = "SELECT COUNT(*) as count FROM PET"
        pet_count = fetch_one(pet_count_query)['count']
        
        # Count total products
        product_count_query = "SELECT COUNT(*) as count FROM PRODUCT"
        product_count = fetch_one(product_count_query)['count']
        
        # Count total users (customers only)
        user_count_query = "SELECT COUNT(*) as count FROM USER WHERE RoleID = 2"
        user_count = fetch_one(user_count_query)['count']
        
        # Count total orders
        order_count_query = "SELECT COUNT(*) as count FROM `ORDER`"
        order_count = fetch_one(order_count_query)['count']
        
       # Get recent orders
        recent_orders_query = """
        SELECT o.*, u.FirstName, u.LastName 
        FROM `ORDER` o
        JOIN USER u ON o.UserID = u.UserID
        ORDER BY o.OrderedDate DESC
        LIMIT 5
        """
        recent_orders = fetch_all(recent_orders_query)
        
        # Get low stock products
        low_stock_query = """
        SELECT p.*, c.CategoryName 
        FROM PRODUCT p
        JOIN CATEGORY c ON p.CategoryID = c.CategoryID
        WHERE p.Stock < 10
        ORDER BY p.Stock ASC
        LIMIT 5
        """
        low_stock_products = fetch_all(low_stock_query)
        
        return render_template('admin/dashboard.html', 
                              pet_count=pet_count,
                              product_count=product_count,
                              user_count=user_count,
                              order_count=order_count,
                              recent_orders=recent_orders,
                              low_stock_products=low_stock_products)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('admin/dashboard.html')

# Pet Management Routes
@admin.route('/pets')
def pets():
    try:
        pet_query = """
        SELECT p.*, b.BreedName
        FROM PET p 
        JOIN BREED b ON p.BreedID = b.BreedID
        ORDER BY p.PetName
        """
        pets = fetch_all(pet_query)
        return render_template('admin/pets.html', pets=pets)
    except Exception as e:
        flash(f'Error loading pets: {str(e)}', 'danger')
        return render_template('admin/pets.html', pets=[])

@admin.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    try:
        # Get all breeds for the dropdown
        breeds_query = "SELECT * FROM BREED ORDER BY BreedName"
        breeds = fetch_all(breeds_query)
        
        if request.method == 'POST':
            pet_name = request.form.get('pet_name')
            breed_id = request.form.get('breed_id')
            age = request.form.get('age')
            price = request.form.get('price')
            
            # Basic validation
            if not all([pet_name, breed_id, age, price]):
                flash('All fields are required', 'danger')
                return render_template('admin/add_pet.html', breeds=breeds)
            
            # Insert new pet
            insert_query = """
            INSERT INTO PET (BreedID, PetName, Age, Price)
            VALUES (%s, %s, %s, %s)
            """
            execute_query(insert_query, (breed_id, pet_name, age, price))
            
            flash('Pet added successfully', 'success')
            return redirect(url_for('admin.pets'))
            
        return render_template('admin/add_pet.html', breeds=breeds)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.pets'))

@admin.route('/pets/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    try:
        # Get pet details
        pet_query = """
        SELECT * FROM PET WHERE PetID = %s
        """
        pet = fetch_one(pet_query, (pet_id,))
        
        if not pet:
            flash('Pet not found', 'danger')
            return redirect(url_for('admin.pets'))
        
        # Get all breeds for the dropdown
        breeds_query = "SELECT * FROM BREED ORDER BY BreedName"
        breeds = fetch_all(breeds_query)
        
        if request.method == 'POST':
            pet_name = request.form.get('pet_name')
            breed_id = request.form.get('breed_id')
            age = request.form.get('age')
            price = request.form.get('price')
            
            # Basic validation
            if not all([pet_name, breed_id, age, price]):
                flash('All fields are required', 'danger')
                return render_template('admin/edit_pet.html', pet=pet, breeds=breeds)
            
            # Update pet
            update_query = """
            UPDATE PET 
            SET BreedID = %s, PetName = %s, Age = %s, Price = %s
            WHERE PetID = %s
            """
            execute_query(update_query, (breed_id, pet_name, age, price, pet_id))
            
            flash('Pet updated successfully', 'success')
            return redirect(url_for('admin.pets'))
            
        return render_template('admin/edit_pet.html', pet=pet, breeds=breeds)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.pets'))

@admin.route('/pets/delete/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    try:
        # Check if pet exists
        check_query = "SELECT * FROM PET WHERE PetID = %s"
        pet = fetch_one(check_query, (pet_id,))
        
        if not pet:
            flash('Pet not found', 'danger')
            return redirect(url_for('admin.pets'))
        
        # Check if pet is in any orders
        order_check_query = "SELECT * FROM ORDERPET WHERE PetID = %s LIMIT 1"
        in_order = fetch_one(order_check_query, (pet_id,))
        
        if in_order:
            flash('Cannot delete pet as it is part of an existing order', 'danger')
            return redirect(url_for('admin.pets'))
        
        # Delete pet
        delete_query = "DELETE FROM PET WHERE PetID = %s"
        execute_query(delete_query, (pet_id,))
        
        flash('Pet deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        
    return redirect(url_for('admin.pets'))

# Product Management Routes
@admin.route('/products')
def products():
    try:
        product_query = """
        SELECT p.*, c.CategoryName
        FROM PRODUCT p 
        JOIN CATEGORY c ON p.CategoryID = c.CategoryID
        ORDER BY p.ProductName
        """
        products = fetch_all(product_query)
        return render_template('admin/products.html', products=products)
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'danger')
        return render_template('admin/products.html', products=[])

@admin.route('/products/add', methods=['GET', 'POST'])
def add_product():
    try:
        # Get all categories for the dropdown
        categories_query = "SELECT * FROM CATEGORY ORDER BY CategoryName"
        categories = fetch_all(categories_query)
        
        if request.method == 'POST':
            product_name = request.form.get('product_name')
            category_id = request.form.get('category_id')
            description = request.form.get('description')
            price = request.form.get('price')
            stock = request.form.get('stock')
            
            # Basic validation
            if not all([product_name, category_id, price, stock]):
                flash('Product name, category, price and stock are required', 'danger')
                return render_template('admin/add_product.html', categories=categories)
            
            # Insert new product
            insert_query = """
            INSERT INTO PRODUCT (CategoryID, ProductName, Description, Price, Stock)
            VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(insert_query, (category_id, product_name, description, price, stock))
            
            flash('Product added successfully', 'success')
            return redirect(url_for('admin.products'))
            
        return render_template('admin/add_product.html', categories=categories)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.products'))

@admin.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    try:
        # Get product details
        product_query = """
        SELECT * FROM PRODUCT WHERE ProductID = %s
        """
        product = fetch_one(product_query, (product_id,))
        
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('admin.products'))
        
        # Get all categories for the dropdown
        categories_query = "SELECT * FROM CATEGORY ORDER BY CategoryName"
        categories = fetch_all(categories_query)
        
        if request.method == 'POST':
            product_name = request.form.get('product_name')
            category_id = request.form.get('category_id')
            description = request.form.get('description')
            price = request.form.get('price')
            stock = request.form.get('stock')
            
            # Basic validation
            if not all([product_name, category_id, price, stock]):
                flash('Product name, category, price and stock are required', 'danger')
                return render_template('admin/edit_product.html', product=product, categories=categories)
            
            # Update product
            update_query = """
            UPDATE PRODUCT 
            SET CategoryID = %s, ProductName = %s, Description = %s, Price = %s, Stock = %s
            WHERE ProductID = %s
            """
            execute_query(update_query, (category_id, product_name, description, price, stock, product_id))
            
            flash('Product updated successfully', 'success')
            return redirect(url_for('admin.products'))
            
        return render_template('admin/edit_product.html', product=product, categories=categories)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.products'))

@admin.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        # Check if product exists
        check_query = "SELECT * FROM PRODUCT WHERE ProductID = %s"
        product = fetch_one(check_query, (product_id,))
        
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('admin.products'))
        
        # Check if product is in any orders
        order_check_query = "SELECT * FROM ORDERPRODUCT WHERE ProductID = %s LIMIT 1"
        in_order = fetch_one(order_check_query, (product_id,))
        
        if in_order:
            flash('Cannot delete product as it is part of an existing order', 'danger')
            return redirect(url_for('admin.products'))
        
        # Delete product
        delete_query = "DELETE FROM PRODUCT WHERE ProductID = %s"
        execute_query(delete_query, (product_id,))
        
        flash('Product deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        
    return redirect(url_for('admin.products'))

# Order Management
@admin.route('/orders')
def orders():
    try:
        orders_query = """
        SELECT o.*, u.FirstName, u.LastName, 
               p.PaymentMethod, p.Status as PaymentStatus
        FROM `ORDER` o
        JOIN USER u ON o.UserID = u.UserID
        JOIN PAYMENT p ON o.PaymentID = p.PaymentID
        ORDER BY o.OrderedDate DESC
        """
        orders = fetch_all(orders_query)
        return render_template('admin/orders.html', orders=orders)
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'danger')
        return render_template('admin/orders.html', orders=[])

@admin.route('/orders/<int:order_id>')
def order_detail(order_id):
    try:
        # Get order details
        order_query = """
        SELECT o.*, u.FirstName, u.LastName, u.Email, u.Phone,
               p.PaymentMethod, p.Status as PaymentStatus, p.Amount as PaymentAmount
        FROM `ORDER` o
        JOIN USER u ON o.UserID = u.UserID
        JOIN PAYMENT p ON o.PaymentID = p.PaymentID
        WHERE o.OrderID = %s
        """
        order = fetch_one(order_query, (order_id,))
        
        if not order:
            flash('Order not found', 'danger')
            return redirect(url_for('admin.orders'))
        
        # Get ordered pets
        pet_items_query = """
        SELECT op.*, p.PetName, p.Price, b.BreedName
        FROM ORDERPET op
        JOIN PET p ON op.PetID = p.PetID
        JOIN BREED b ON p.BreedID = b.BreedID
        WHERE op.OrderID = %s
        """
        pet_items = fetch_all(pet_items_query, (order_id,))
        
        # Get ordered products
        product_items_query = """
        SELECT op.*, p.ProductName, p.Price, c.CategoryName
        FROM ORDERPRODUCT op
        JOIN PRODUCT p ON op.ProductID = p.ProductID
        JOIN CATEGORY c ON p.CategoryID = c.CategoryID
        WHERE op.OrderID = %s
        """
        product_items = fetch_all(product_items_query, (order_id,))
        
        return render_template('admin/order_detail.html', 
                              order=order, 
                              pet_items=pet_items, 
                              product_items=product_items)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.orders'))

@admin.route('/orders/update-status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    try:
        # Check if order exists
        check_query = "SELECT * FROM `ORDER` WHERE OrderID = %s"
        order = fetch_one(check_query, (order_id,))
        
        if not order:
            flash('Order not found', 'danger')
            return redirect(url_for('admin.orders'))
        
        order_status = request.form.get('order_status')
        delivery_status = request.form.get('delivery_status')
        
        # Update order status
        update_query = """
        UPDATE `ORDER` 
        SET OrderStatus = %s, DeliveryStatus = %s
        WHERE OrderID = %s
        """
        execute_query(update_query, (order_status, delivery_status, order_id))
        
        flash('Order status updated successfully', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        
    return redirect(url_for('admin.order_detail', order_id=order_id))