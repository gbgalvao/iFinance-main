import jwt

from datetime import date, datetime, timedelta
from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import admin_required, token_required, brl, find_number, find_special_char

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["brl"] = brl

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
Session(app)

db = SQLAlchemy(app)

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50))
   username = db.Column(db.String(50), unique=True)
   hash = db.Column(db.String(170), unique=True)
   admin = db.Column(db.Boolean, default=False)
   date_joined = db.Column(db.Date)
   expenses = db.relationship('Expenses', backref='user')
   
class Expense_category(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50))
   expenses = db.relationship('Expenses', backref='category')

class Expenses(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
   name = db.Column(db.String(50))
   price = db.Column(db.Float)
   date = db.Column(db.Date)
   category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id'))

with app.app_context():
   db.create_all()

@app.route("/")
@token_required
def index(current_user):
  """"Show table of expenses and add/remove more expenses"""
  if request.method == "GET":
      try:
         Expense_list_db = Expenses.query.filter(Expenses.user_id == current_user).all()
         expenses = []
         for expense in Expense_list_db:
            expense_category_name = Expense_category.query.filter(Expense_category.id == expense.category_id).with_entities(Expense_category.name).first()
            expense_info = {
               "name": expense.name,
               "category": expense_category_name.name,
               "price": expense.price,
               "date": expense.date
            }
            expenses.append(expense_info)

         return jsonify(expenses)
      
      except:
         return jsonify({'message': "Some error ocurred"}), 500

@app.route("/login", methods=["POST", "GET"])
def login():
    """Log in User"""

    # Forget any user_id
    session.clear()

    # If request comes from a get method the login form is displayed
    if request.method == "GET":
      return render_template("login.html")
    
    # If request comes from a post method login form will be sent
    else:
      # Getting login info
      login_info = request.json

      username = login_info.get('username')
      password = login_info.get('password')

      if not username or not password:
            return jsonify({'message': 'Invalid username or password'}), 403
      
      # Query database for username *TODO*
      user = Users.query.filter(Users.username == username).first()

      if user is None or not check_password_hash(user.hash, password):
            return jsonify({'message': 'Invalid username or password'}), 403

      # Create a payload for the token
      payload = {
         'user_id': user.id,
         'admin': user.admin,
         'exp': datetime.now() + timedelta(hours=24)  # Set expiration time
      }

      # Generate the token
      token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')

      # Return the token
      return jsonify({'token': token}), 200
    

@app.route("/logout", methods=["POST"])
@token_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route("/register", methods=["POST", "GET"])
def register():
   """Register User"""
   
   # If request comes from a get method the register form is displayed
   if request.method == "GET":
    return render_template("register.html")
   
   # If request comes from a post method register form will be sent
   else:
      register_info = request.json

      name = register_info.get('name')
      username = register_info.get('username')
      password = register_info.get('password')
      confirmation = register_info.get('confirmation')

      if not name or not name.isalpha():
         return jsonify("Use only letters for your name"), 403

      elif not username:
         return 401
      
      elif not password:
         return 402
      
      elif len(password) < 8 or find_special_char(password) == False or find_number(password) == False:
         return jsonify({"message": "Password must contain at least 8 characters, numbers and special characters"}), 402
      
      elif confirmation != password:
         return jsonify({"message": "Password don't match"}), 406     
      else:
         user = Users(name=name, username=username, hash=generate_password_hash(password), date_joined=date.today())

         try:
            db.session.add(user)
            db.session.commit()
            return jsonify("Success"), 200
         except ValueError:
            return jsonify("Some error ocurred"), 400


@app.route("/add_category", methods=["POST"])
@token_required
@admin_required
def add_category(current_user, admin):
   category_json  = request.json.get('category').lower()
   category = Expense_category(name=category_json)
   categories_query = db.session.query(Expense_category.name).all()
   categories = [category[0] for category in categories_query]

   if not category_json:
      return jsonify("Can't be empty"), 403
   elif not isinstance(category_json, str):
    return jsonify("Category should be a string"), 400
   elif not category_json.isalpha():
      return jsonify("Only alphabetic characters allowed"), 403
   elif not (1 <= len(category_json) <= 50):
      return jsonify("Category length should be between 1 and 50 characters"), 400
   elif category_json in categories:
      return jsonify("Category already exists"), 403
   else:
      try:
         db.session.add(category)
         db.session.commit()
         return jsonify("Category added"), 200
      except ValueError:
         return jsonify("Some error ocurred"), 400
      
@app.route("/delete_category", methods=["POST"])
@token_required
@admin_required
def delete_category(current_user, admin):
   category  = request.json.get('category').lower()
   categories_query = db.session.query(Expense_category.name).all()
   categories = [category[0] for category in categories_query]

   if not category:
      return jsonify("Can't be empty"), 403
   elif not isinstance(category, str):
    return jsonify("Category should be a string"), 400
   elif not category.isalpha():
      return jsonify("Only alphabetic characters allowed"), 403
   elif not (1 <= len(category) <= 50):
      return jsonify("Category length should be between 1 and 50 characters"), 400
   elif category not in categories:
      return jsonify("Category not found"), 404
   else:
      try:
         db.session.query(Expense_category).filter(Expense_category.name == category).delete()
         db.session.commit()   
         return jsonify("Category deleted"), 200
      except ValueError:
         return jsonify("Some error ocurred"), 400
   

   
@app.route("/add_expense", methods=["POST"])
@token_required
def add_expense(current_user):
   categories = Expense_category.query.all()

   expense_data = request.json

   if expense_data['category'] not in [category.name for category in categories]:
        return jsonify("Category not available"), 404
   if not expense_data["name"] or not expense_data["category"]:
      return jsonify("Name or category fields can't be null"), 403
    
   try:
      price = float(expense_data["price"])
      if price <= 0:
         return jsonify("Price can't be 0 or lower"), 403
   except ValueError:
      return jsonify("Some error ocurred"), 400

   try:
      expense_date = datetime.strptime(expense_data["date"], "%Y-%m-%d").date()
      if expense_date > date.today():
         return jsonify("Date can't be in the future"), 403
   except ValueError:
      return jsonify("Some error ocurred"), 400

   category = Expense_category.query.filter_by(name=expense_data["category"]).first()
   if not category:
      return jsonify("Some error ocurred"), 400

   expense_data_db = Expenses(
      user_id=current_user,
      name=expense_data["name"],
      price=price,
      date=expense_date,
      category_id=category.id
   )

   try:
      db.session.add(expense_data_db)
      db.session.commit()

      return jsonify("Success"), 200
   except ValueError:
      return jsonify("Some error ocurred"), 400


@app.route("/get_categories")
@token_required
def get_categories(current_user):
    categories = Expense_category.query.all()  # Fetch categories from your database
    category_names = [category.name for category in categories]

    return jsonify({'categories': category_names})


# Chartview route
@app.route("/chartview")
@token_required
def chartview(current_user):
   years_query = db.session.query(func.extract('year', Expenses.date)).filter(Expenses.user_id == current_user).distinct()
   years = [result[0] for result in years_query]

   return jsonify(years)


@app.route("/fetch_data", methods=["POST"])
@token_required
def fetch_data():
   return 200

# Route used by chartview
@app.route("/fetch_data_chart", methods=["POST"])
@token_required
def fetch_data_chart(current_user):
      if request.method == "POST":
         year = request.json.get("year")  # Access JSON data from the request body

         data_query = (
            db.session.query(
               func.extract('year', Expenses.date).label('year'),
               func.extract('month', Expenses.date).label('month'),
               func.sum(Expenses.price).label('total_value')
            )
            .filter(
               func.extract('year', Expenses.date) == year,
               Expenses.user_id == current_user  # Ensure user_id condition placement
            )
            .group_by('year', 'month')
            .order_by('year', 'month')
         )

         data_query_sum = data_query.all()

         data = []

         for result in data_query_sum:
            data_sum = {
               'year': result.year,
               'month': result.month,
               'total_value': f'{result.total_value:.2f}'
            }
            data.append(data_sum)
         
         if not data:
            return jsonify(f"{'No data available for the year: ', year}"), 404
         else:
            return jsonify(data)
      
@app.route("/manage_users")
@token_required
@admin_required
def manage_users(current_user, admin):
   users_query = db.session.query(Users.name , Users.username, Users.date_joined).all()

   users = []
   for user in users_query:
      result = {
         "name": user.name,
         "username": user.username,
         "date_joined": user.date_joined
      }
      users.append(result)

   try:
      return jsonify(users), 200
   except ValueError:
      return jsonify("Some error ocurred"), 400

@app.route("/delete_user", methods=["POST"])
@token_required
@admin_required
def delete_user(current_user, admin):
   username_to_delete = request.json.get("username_to_delete")

   username_to_delete_query = db.session.query(Users).filter(Users.username == username_to_delete).first()

   if username_to_delete_query:
      try:
         db.session.delete(username_to_delete_query)
         db.session.commit()
         return jsonify("User deleted succesfully")
      except ValueError:
         return jsonify("An error occured"), 400
      
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
   