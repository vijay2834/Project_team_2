# routes/pet.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from routes import fetch_all, fetch_one

pet = Blueprint('pet', __name__, url_prefix='/pets')

@pet.route('/')
def list():
    # Get all breeds for filtering
    breed_query = "SELECT * FROM BREED ORDER BY BreedName"
    breeds = fetch_all(breed_query)
    
    # Get filter parameters
   # routes/pet.py (continued)
    # Get filter parameters
    breed_id = request.args.get('breed_id', type=int)
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Build base query
    query = """
    SELECT p.*, b.BreedName
    FROM PET p
    JOIN BREED b ON p.BreedID = b.BreedID
    WHERE 1=1
    """
    params = []
    
    # Add filters if provided
    if breed_id:
        query += " AND p.BreedID = %s"
        params.append(breed_id)
    
    if min_age:
        query += " AND p.Age >= %s"
        params.append(min_age)
        
    if max_age:
        query += " AND p.Age <= %s"
        params.append(max_age)
    
    if min_price:
        query += " AND p.Price >= %s"
        params.append(min_price)
        
    if max_price:
        query += " AND p.Price <= %s"
        params.append(max_price)
    
    # Add sorting
    query += " ORDER BY p.PetName"
    
    # Execute query
    pets = fetch_all(query, tuple(params) if params else None)
    
    return render_template('pets/pet_list.html', pets=pets, breeds=breeds)

@pet.route('/<int:pet_id>')
def detail(pet_id):
    # Get pet details
    query = """
    SELECT p.*, b.BreedName
    FROM PET p
    JOIN BREED b ON p.BreedID = b.BreedID
    WHERE p.PetID = %s
    """
    pet = fetch_one(query, (pet_id,))
    
    if not pet:
        flash('Pet not found.', 'danger')
        return redirect(url_for('pet.list'))
    
    # Get recommended products for this pet
    # For example, products in the same category as pets (food, toys, etc.)
    product_query = """
    SELECT p.*, c.CategoryName
    FROM PRODUCT p
    JOIN CATEGORY c ON p.CategoryID = c.CategoryID
    ORDER BY RAND()
    LIMIT 4
    """
    recommended_products = fetch_all(product_query)
    
    return render_template('pets/pet_detail.html', 
                           pet=pet, 
                           recommended_products=recommended_products)