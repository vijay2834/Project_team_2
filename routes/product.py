# routes/product.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from routes import fetch_all, fetch_one

product = Blueprint('product', __name__, url_prefix='/products')

@product.route('/')
def list():
    # Get all categories for filtering
    category_query = "SELECT * FROM CATEGORY ORDER BY CategoryName"
    categories = fetch_all(category_query)
    
    # Get filter parameters
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'name_asc')
    
    # Build base query
    query = """
    SELECT p.*, c.CategoryName
    FROM PRODUCT p
    JOIN CATEGORY c ON p.CategoryID = c.CategoryID
    WHERE 1=1
    """
    params = []
    
    # Add filters if provided
    if category_id:
        query += " AND p.CategoryID = %s"
        params.append(category_id)
    
    if min_price:
        query += " AND p.Price >= %s"
        params.append(min_price)
        
    if max_price:
        query += " AND p.Price <= %s"
        params.append(max_price)
    
    # Add sorting
    if sort == 'name_asc':
        query += " ORDER BY p.ProductName ASC"
    elif sort == 'name_desc':
        query += " ORDER BY p.ProductName DESC"
    elif sort == 'price_asc':
        query += " ORDER BY p.Price ASC"
    elif sort == 'price_desc':
        query += " ORDER BY p.Price DESC"
    else:
        query += " ORDER BY p.ProductName ASC"
    
    # Execute query
    products = fetch_all(query, tuple(params) if params else None)
    
    return render_template('products/product_list.html', 
                           products=products, 
                           categories=categories)

@product.route('/<int:product_id>')
def detail(product_id):
    # Get product details
    query = """
    SELECT p.*, c.CategoryName
    FROM PRODUCT p
    JOIN CATEGORY c ON p.CategoryID = c.CategoryID
    WHERE p.ProductID = %s
    """
    product = fetch_one(query, (product_id,))
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('product.list'))
    
    # Get similar products (same category)
    similar_query = """
    SELECT p.*, c.CategoryName
    FROM PRODUCT p
    JOIN CATEGORY c ON p.CategoryID = c.CategoryID
    WHERE p.CategoryID = %s AND p.ProductID != %s
    ORDER BY RAND()
    LIMIT 4
    """
    similar_products = fetch_all(similar_query, (product['CategoryID'], product_id))
    
    return render_template('products/product_detail.html', 
                           product=product, 
                           similar_products=similar_products)