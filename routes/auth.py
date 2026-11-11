from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import datetime
import re
from routes import execute_query, fetch_one, verify_password, hash_password

auth = Blueprint('auth', __name__, url_prefix='/auth')

def validate_password_strength(password):
    """
    Validate password strength against multiple criteria
    Returns (is_valid, error_message)
    """
    # Check length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    
    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    
    # Check for at least one digit
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    
    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    
    return True, ""

def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Simple validation to ensure it contains only digits and common separators
    phone_clean = re.sub(r'[\s\-\(\)\.]', '', phone)
    return phone_clean.isdigit() and len(phone_clean) >= 10

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            # Validate form data
            errors = []
            if not email:
                errors.append('Email is required.')
            elif not validate_email(email):
                errors.append('Please enter a valid email address.')
                
            if not password:
                errors.append('Password is required.')
                
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('auth/login.html')
            
            # Query database for user
            query = "SELECT * FROM USER WHERE Email = %s"
            user = fetch_one(query, (email,))
            
            # Check if user exists and password is correct
            if user and verify_password(user['Password'], password):
                # Set session variables
                session['logged_in'] = True
                session['user_id'] = user['UserID']
                session['user_name'] = f"{user['FirstName']} {user['LastName']}"
                session['is_admin'] = user['RoleID'] == 1
                
                flash('Login successful!', 'success')
                
                 # Redirect to admin dashboard if admin, else redirect to the main index
                if session['is_admin']:
                    return redirect(url_for('auth.admin_dashboard'))  # Redirect to admin dashboard
                else:
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect(url_for('main.index'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
                
        except Exception as e:
            flash('An unexpected error occurred. Please try again later.', 'danger')
            print(f"Login error: {str(e)}")
    
    return render_template('auth/login.html')

@auth.route('/admin_dashboard')
def admin_dashboard():
    # Ensure the user is an admin
    if not session.get('is_admin', False):  
        flash('Access denied. You must be an admin to view this page.', 'danger')
        return redirect(url_for('main.index'))  # Redirect to general user page if not admin

    return render_template('admin/dashboard.html')  # Admin-specific dashboard template


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validate form data
            errors = []
            
            if not first_name:
                errors.append('First name is required.')
            elif len(first_name) < 2:
                errors.append('First name must be at least 2 characters long.')
                
            if not last_name:
                errors.append('Last name is required.')
            elif len(last_name) < 2:
                errors.append('Last name must be at least 2 characters long.')
                
            if not email:
                errors.append('Email is required.')
            elif not validate_email(email):
                errors.append('Please enter a valid email address.')
                
            if not phone:
                errors.append('Phone number is required.')
            elif not validate_phone(phone):
                errors.append('Please enter a valid phone number.')
                
            if not password:
                errors.append('Password is required.')
            else:
                # Validate password strength
                is_strong, pwd_error = validate_password_strength(password)
                if not is_strong:
                    errors.append(pwd_error)
                    
            if password != confirm_password:
                errors.append('Passwords do not match.')
                
            # If there are validation errors, display them and return to the form
            if errors:
                for error in errors:
                    flash(error, 'danger')
                # Return form with previously entered data for better UX
                return render_template('auth/register.html', 
                                      first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      phone=phone)
            
            # Check if user already exists
            check_query = "SELECT * FROM USER WHERE Email = %s"
            existing_user = fetch_one(check_query, (email,))
            
            if existing_user:
                flash('Email already in use. Please use a different email or login.', 'danger')
                return render_template('auth/register.html',
                                      first_name=first_name,
                                      last_name=last_name,
                                      phone=phone)
            
            # Insert new user with a salted password hash
            now = datetime.datetime.now()
            insert_query = """
            INSERT INTO USER (RoleID, FirstName, LastName, Email, Phone, Password, CreatedDateTime) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            user_id = execute_query(insert_query, (2, first_name, last_name, email, phone, hash_password(password), now))
            
            # Set session variables to automatically login
            session['logged_in'] = True
            session['user_id'] = user_id
            session['user_name'] = f"{first_name} {last_name}"
            session['is_admin'] = False
            
            flash('Registration successful! Welcome to Pet Connect.', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            flash('An unexpected error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {str(e)}")
            # Log the detailed error for debugging but don't show to user
    
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    try:
        # Clear session data
        session.clear()
        flash('You have been logged out.', 'info')
    except Exception as e:
        flash('An error occurred during logout.', 'danger')
        print(f"Logout error: {str(e)}")
    
    return redirect(url_for('main.index'))