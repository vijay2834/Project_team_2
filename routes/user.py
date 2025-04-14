# routes/user.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from routes import execute_query, fetch_all, fetch_one
import datetime

user = Blueprint('user', __name__, url_prefix='/user')

# Authentication middleware
@user.before_request
def check_authenticated():
    if 'logged_in' not in session:
        flash('Please log in to access your profile', 'warning')
        return redirect(url_for('auth.login'))

@user.route('/profile')
def profile():
    try:
        # Get user information
        query = "SELECT * FROM USER WHERE UserID = %s"
        user_data = fetch_one(query, (session['user_id'],))
        
        if not user_data:
            flash('User not found', 'danger')
            return redirect(url_for('main.index'))
        
        # Get user addresses
        addresses_query = """
        SELECT * FROM ADDRESS 
        WHERE UserID = %s
        ORDER BY CurrentYesOrNo DESC
        """
        addresses = fetch_all(addresses_query, (session['user_id'],))
        
        return render_template('user/profile.html', user=user_data, addresses=addresses)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

@user.route('/profile/update', methods=['POST'])
def update_profile():
    try:
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Basic validation
        if not all([first_name, last_name, email, phone]):
            flash('All fields are required', 'danger')
            return redirect(url_for('user.profile'))
        
        # Update user information
        update_query = """
        UPDATE USER 
        SET FirstName = %s, LastName = %s, Email = %s, Phone = %s 
        WHERE UserID = %s
        """
        execute_query(update_query, (first_name, last_name, email, phone, session['user_id']))
        
        # Update session
        session['user_name'] = f"{first_name} {last_name}"
        
        flash('Profile updated successfully', 'success')
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'danger')
    
    return redirect(url_for('user.profile'))

@user.route('/profile/change-password', methods=['POST'])
def change_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not all([current_password, new_password, confirm_password]):
            flash('All password fields are required', 'danger')
            return redirect(url_for('user.profile'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('user.profile'))
        
        # Get current user password
        query = "SELECT Password FROM USER WHERE UserID = %s"
        user = fetch_one(query, (session['user_id'],))
        
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('user.profile'))
        
        # Check current password
        if user['Password'] != current_password:
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('user.profile'))
        
        # Update password
        update_query = """
        UPDATE USER 
        SET Password = %s 
        WHERE UserID = %s
        """
        execute_query(update_query, (new_password, session['user_id']))
        
        flash('Password updated successfully', 'success')
    except Exception as e:
        flash(f'Error changing password: {str(e)}', 'danger')
    
    return redirect(url_for('user.profile'))

@user.route('/addresses')
def addresses():
    try:
        # Get user addresses
        query = """
        SELECT * FROM ADDRESS 
        WHERE UserID = %s
        ORDER BY CurrentYesOrNo DESC
        """
        addresses = fetch_all(query, (session['user_id'],))
        
        return render_template('user/addresses.html', addresses=addresses)
    except Exception as e:
        flash(f'Error loading addresses: {str(e)}', 'danger')
        return redirect(url_for('user.profile'))

@user.route('/addresses/add', methods=['POST'])
def add_address():
    try:
        # Get form data
        street1 = request.form.get('street1')
        street2 = request.form.get('street2', '')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')
        is_default = request.form.get('is_default') == 'on'
        
        # Basic validation
        if not all([street1, city, state, zip_code]):
            flash('Street, city, state and zip are required', 'danger')
            return redirect(url_for('user.addresses'))
        
        # If setting as default, update all existing addresses
        if is_default:
            update_query = """
            UPDATE ADDRESS 
            SET CurrentYesOrNo = 0 
            WHERE UserID = %s
            """
            execute_query(update_query, (session['user_id'],))
        
        # Insert new address
        insert_query = """
        INSERT INTO ADDRESS (UserID, Street1, Street2, City, State, Zip, CurrentYesOrNo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(insert_query, (session['user_id'], street1, street2, city, state, zip_code, is_default))
        
        flash('Address added successfully', 'success')
    except Exception as e:
        flash(f'Error adding address: {str(e)}', 'danger')
    
    return redirect(url_for('user.addresses'))

@user.route('/addresses/delete/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    try:
        # Check if address belongs to user
        check_query = """
        SELECT * FROM ADDRESS 
        WHERE AddressID = %s AND UserID = %s
        """
        address = fetch_one(check_query, (address_id, session['user_id']))
        
        if not address:
            flash('Address not found or does not belong to you', 'danger')
            return redirect(url_for('user.addresses'))
        
        # Delete address
        delete_query = "DELETE FROM ADDRESS WHERE AddressID = %s"
        execute_query(delete_query, (address_id,))
        
        flash('Address deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting address: {str(e)}', 'danger')
    
    return redirect(url_for('user.addresses'))

@user.route('/addresses/set-default/<int:address_id>', methods=['POST'])
def set_default_address(address_id):
    try:
        # Check if address belongs to user
        check_query = """
        SELECT * FROM ADDRESS 
        WHERE AddressID = %s AND UserID = %s
        """
        address = fetch_one(check_query, (address_id, session['user_id']))
        
        if not address:
            flash('Address not found or does not belong to you', 'danger')
            return redirect(url_for('user.addresses'))
        
        # Reset all addresses first
        reset_query = """
        UPDATE ADDRESS 
        SET CurrentYesOrNo = 0 
        WHERE UserID = %s
        """
        execute_query(reset_query, (session['user_id'],))
        
        # Set selected address as default
        update_query = """
        UPDATE ADDRESS 
        SET CurrentYesOrNo = 1 
        WHERE AddressID = %s
        """
        execute_query(update_query, (address_id,))
        
        flash('Default address updated successfully', 'success')
    except Exception as e:
        flash(f'Error updating default address: {str(e)}', 'danger')
    
    return redirect(url_for('user.addresses'))

@user.route('/orders')
def orders():
    try:
        # Get user orders
        query = """
        SELECT o.*, p.PaymentMethod, p.Status as PaymentStatus 
        FROM `ORDER` o
        JOIN PAYMENT p ON o.PaymentID = p.PaymentID
        WHERE o.UserID = %s
        ORDER BY o.OrderedDate DESC
        """
        orders_list = fetch_all(query, (session['user_id'],))
        
        return render_template('user/orders.html', orders=orders_list)
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'danger')
        return redirect(url_for('user.profile'))

@user.route('/orders/<int:order_id>')
def order_detail(order_id):
    try:
        # Get order details, ensuring it belongs to the user
        order_query = """
        SELECT o.*, p.PaymentMethod, p.Status as PaymentStatus, p.Amount as PaymentAmount
        FROM `ORDER` o
        JOIN PAYMENT p ON o.PaymentID = p.PaymentID
        WHERE o.OrderID = %s AND o.UserID = %s
        """
        order = fetch_one(order_query, (order_id, session['user_id']))
        
        if not order:
            flash('Order not found or does not belong to you', 'danger')
            return redirect(url_for('user.orders'))
        
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
        
        return render_template('user/order_detail.html', 
                               order=order, 
                               pet_items=pet_items, 
                               product_items=product_items)
    except Exception as e:
        flash(f'Error loading order details: {str(e)}', 'danger')
        return redirect(url_for('user.orders'))