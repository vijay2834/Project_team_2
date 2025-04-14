# routes/main.py
from flask import Blueprint, render_template
from routes import fetch_all

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Fetch featured pets (4 random pets)
    pet_query = """
    SELECT p.*, b.BreedName
    FROM PET p
    JOIN BREED b ON p.BreedID = b.BreedID
    ORDER BY RAND()
    LIMIT 4
    """
    featured_pets = fetch_all(pet_query)
    
    # Add image placeholder
    for pet in featured_pets:
        id = str(pet['BreedID'])
        pet['image'] = f'{id}.png'
    
    # Fetch featured products (4 random products)
    product_query = """
    SELECT p.*, c.CategoryName
    FROM PRODUCT p
    JOIN CATEGORY c ON p.CategoryID = c.CategoryID
    ORDER BY RAND()
    LIMIT 4
    """
    featured_products = fetch_all(product_query)
    
    # Add image placeholder
    for product in featured_products:
        id = str(product['ProductID'])
        product['image'] = f'{id}.png'
    
    return render_template('index.html', 
                           featured_pets=featured_pets,
                           featured_products=featured_products)