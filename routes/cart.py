# routes/cart.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from routes import execute_query, fetch_all, fetch_one
import datetime
import json

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/')
def view():
    cart_items = []
    total = 0
    
    if 'cart' in session and session['cart']:
        try:
            # Process pets in cart
            pet_ids = [item['id'] for item in session['cart'] if item['type'] == 'pet']
            if pet_ids:
                # Get pet details
                pets_list = []
                for pet_id in pet_ids:
                    query = """
                    SELECT p.*, b.BreedName
                    FROM PET p
                    JOIN BREED b ON p.BreedID = b.BreedID
                    WHERE p.PetID = %s
                    """
                    pet = fetch_one(query, (pet_id,))
                    if pet:
                        pets_list.append(pet)
                
                # Build pet dictionary for easy lookup
                pet_dict = {pet['PetID']: pet for pet in pets_list}
                
                # Add pet items to cart_items
                for item in session['cart']:
                    if item['type'] == 'pet' and item['id'] in pet_dict:
                        pet = pet_dict[item['id']]
                        item_total = pet['Price'] * item['quantity']
                        total += item_total
                        
                        cart_items.append({
                            'id': pet['PetID'],
                            'BreedID':pet['BreedID'],
                            'name': pet['PetName'],
                            'breed': pet['BreedName'],
                            'price': pet['Price'],
                            'quantity': item['quantity'],
                            'total': item_total,
                            'type': 'pet'
                        })
            
            # Process products in cart
            product_ids = [item['id'] for item in session['cart'] if item['type'] == 'product']
            if product_ids:
                # Get product details
                products_list = []
                for product_id in product_ids:
                    query = """
                    SELECT p.*, c.CategoryName
                    FROM PRODUCT p
                    JOIN CATEGORY c ON p.CategoryID = c.CategoryID
                    WHERE p.ProductID = %s
                    """
                    product = fetch_one(query, (product_id,))
                    if product:
                        products_list.append(product)
                
                # Build product dictionary for easy lookup
                product_dict = {product['ProductID']: product for product in products_list}
                
                # Add product items to cart_items
                for item in session['cart']:
                    if item['type'] == 'product' and item['id'] in product_dict:
                        product = product_dict[item['id']]
                        item_total = product['Price'] * item['quantity']
                        total += item_total
                        
                        cart_items.append({
                            'id': product['ProductID'],
                            'name': product['ProductName'],
                            'category': product['CategoryName'],
                            'price': product['Price'],
                            'quantity': item['quantity'],
                            'total': item_total,
                            'type': 'product'
                        })
        except Exception as e:
            flash(f'Error loading cart: {str(e)}', 'danger')
    
    return render_template('cart/cart.html', cart_items=cart_items, total=total)

@cart.route('/add', methods=['POST'])
def add():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    try:
        data = request.get_json()
        item_id = data.get('id')
        item_type = data.get('type')
        quantity = int(data.get('quantity', 1))
        
        if not item_id or not item_type:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        # Initialize cart if it doesn't exist
        if 'cart' not in session:
            session['cart'] = []
        
        # Convert item_id to int to ensure consistency
        item_id = int(item_id)
        
        # Check if item exists in database
        if item_type == 'pet':
            query = "SELECT * FROM PET WHERE PetID = %s"
        else:
            query = "SELECT * FROM PRODUCT WHERE ProductID = %s"
        
        item = fetch_one(query, (item_id,))
        
        if not item:
            return jsonify({'success': False, 'message': 'Item not found'})
        
        # Check if item already in cart
        cart_item = next((item for item in session['cart'] 
                          if item['id'] == item_id and item['type'] == item_type), None)
        
        if cart_item:
            # Update quantity
            cart_item['quantity'] += quantity
        else:
            # Add new item
            session['cart'].append({
                'id': item_id,
                'type': item_type,
                'quantity': quantity
            })
        
        session.modified = True
        
        return jsonify({
            'success': True, 
            'message': 'Item added to cart successfully',
            'cart_count': len(session['cart'])
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@cart.route('/update', methods=['POST'])
def update():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    try:
        data = request.get_json()
        item_id = int(data.get('id'))
        item_type = data.get('type')
        quantity = int(data.get('quantity', 1))
        
        if not item_id or not item_type:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        if 'cart' not in session:
            return jsonify({'success': False, 'message': 'Cart is empty'})
        
        # Find and update item
        for item in session['cart']:
            if item['id'] == item_id and item['type'] == item_type:
                item['quantity'] = max(1, min(10, quantity))  # Limit quantity between 1 and 10
                session.modified = True
                break
        
        return jsonify({'success': True, 'message': 'Cart updated successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@cart.route('/remove', methods=['POST'])
def remove():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    try:
        data = request.get_json()
        item_id = int(data.get('id'))
        item_type = data.get('type')
        
        if not item_id or not item_type:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        if 'cart' in session:
            # Remove item from cart
            session['cart'] = [item for item in session['cart'] 
                              if not (item['id'] == item_id and item['type'] == item_type)]
            session.modified = True
        
        return jsonify({'success': True, 'message': 'Item removed from cart'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@cart.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'logged_in' not in session:
        flash('Please log in to checkout', 'warning')
        return redirect(url_for('auth.login'))
    
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'info')
        return redirect(url_for('cart.view'))
    
    # Get cart items and total
    cart_items = []
    total = 0
    
    try:
        # ... [same as view() method to retrieve cart items] ...
        # Process cart items (same code as in view method)
        
        # Add taxes and calculate grand total
        tax_rate = 0.08  # 8% tax
        tax_amount = round(total * tax_rate, 2)
        grand_total = total + tax_amount
        
        # Get user's addresses
        address_query = """
        SELECT * FROM ADDRESS
        WHERE UserID = %s
        ORDER BY CurrentYesOrNo DESC
        """
        addresses = fetch_all(address_query, (session['user_id'],))
        
        if request.method == 'POST':
            # Process the order
            payment_method = request.form.get('payment_method')
            address_id = request.form.get('address_id')
            save_address = request.form.get('save_address') == 'on'
            
            # Validate inputs
            if not payment_method:
                flash('Please select a payment method', 'danger')
                return render_template('cart/checkout.html', 
                                      cart_items=cart_items,
                                      total=total,
                                      tax_amount=tax_amount,
                                      grand_total=grand_total,
                                      addresses=addresses)
            
            # If using a new address, save it
            if address_id == 'new':
                street1 = request.form.get('street1')
                street2 = request.form.get('street2', '')
                city = request.form.get('city')
                state = request.form.get('state')
                zip_code = request.form.get('zip')
                
                if not all([street1, city, state, zip_code]):
                    flash('Please fill in all address fields', 'danger')
                    return render_template('cart/checkout.html', 
                                          cart_items=cart_items,
                                          total=total,
                                          tax_amount=tax_amount,
                                          grand_total=grand_total,
                                          addresses=addresses)
                
                # Insert new address
                address_query = """
                INSERT INTO ADDRESS (UserID, Street1, Street2, City, State, Zip, CurrentYesOrNo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                address_id = execute_query(address_query, (
                    session['user_id'],
                    street1,
                    street2,
                    city,
                    state,
                    zip_code,
                    save_address
                ))
            
            # Create payment record
            payment_query = """
            INSERT INTO PAYMENT (PaymentMethod, Amount, Date, Status)
            VALUES (%s, %s, %s, %s)
            """
            payment_date = datetime.datetime.now()
            payment_status = 'Successful'  # In a real app, this would depend on payment processing
            
            payment_id = execute_query(payment_query, (
                payment_method,
                grand_total,
                payment_date,
                payment_status
            ))
            
            # Create order
            order_query = """
            INSERT INTO `ORDER` (UserID, PaymentID, OrderedDate, TotalAmount, OrderStatus, DeliveryStatus, DeliveryDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            order_date = datetime.datetime.now()
            delivery_date = order_date + datetime.timedelta(days=7)  # Estimated delivery in 7 days
            
            order_id = execute_query(order_query, (
                session['user_id'],
                payment_id,
                order_date,
                grand_total,
                'Pending',  # Initial order status
                'Pending',  # Initial delivery status
                delivery_date
            ))
            
            # Process cart items
            for item in session['cart']:
                if item['type'] == 'pet':
                    # Add to OrderPet table
                    pet_query = "SELECT Price FROM PET WHERE PetID = %s"
                    pet = fetch_one(pet_query, (item['id'],))
                    
                    if pet:
                        total_item_amount = pet['Price'] * item['quantity']
                        order_pet_query = """
                        INSERT INTO ORDERPET (OrderID, PetID, Quantity, TotalItemAmount)
                        VALUES (%s, %s, %s, %s)
                        """
                        execute_query(order_pet_query, (
                            order_id,
                            item['id'],
                            item['quantity'],
                            total_item_amount
                        ))
                else:
                    # Add to OrderProduct table
                    product_query = "SELECT Price, Stock FROM PRODUCT WHERE ProductID = %s"
                    product = fetch_one(product_query, (item['id'],))
                    
                    if product:
                        total_item_amount = product['Price'] * item['quantity']
                        order_product_query = """
                        INSERT INTO ORDERPRODUCT (OrderID, ProductID, Quantity, TotalItemAmount)
                        VALUES (%s, %s, %s, %s)
                        """
                        execute_query(order_product_query, (
                            order_id,
                            item['id'],
                            item['quantity'],
                            total_item_amount
                        ))
                        
                        # Update product stock
                        new_stock = product['Stock'] - item['quantity']
                        update_stock_query = """
                        UPDATE PRODUCT SET Stock = %s WHERE ProductID = %s
                        """
                        execute_query(update_stock_query, (new_stock, item['id']))
            
            # Clear the cart
            session.pop('cart', None)
            
            flash('Order placed successfully! Thank you for your purchase.', 'success')
            return redirect(url_for('user.order_detail', order_id=order_id))
        
        return render_template('cart/checkout.html', 
                              cart_items=cart_items,
                              total=total,
                              tax_amount=tax_amount,
                              grand_total=grand_total,
                              addresses=addresses)
                              
    except Exception as e:
        flash(f'Error processing checkout: {str(e)}', 'danger')
        return redirect(url_for('cart.view'))