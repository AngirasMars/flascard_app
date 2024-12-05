from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # For session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'  # Use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect unauthorized users to login page

# Define the User model with the 'role' column
class User(UserMixin, db.Model):
    id = db.Column(db.String(150), primary_key=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50), default='user')  # Default role is 'user'

    def check_password(self, password):
        return self.password == password

# Load user for Flask-Login
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

# Flashcard model
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.String(300), nullable=False)

# Home route - Flashcards Page
@app.route('/flashcards', methods=['GET'])
@login_required
def flashcards():
    # Get index from URL parameters (default to 0 if not provided)
    index = request.args.get('index', 0, type=int)

    # Fetch all flashcards from the database
    flashcards = Flashcard.query.all()

    # Ensure there are flashcards in the database
    if not flashcards:
        return render_template('flashcards.html', error="No flashcards available.")

    # Get the total number of flashcards
    total_flashcards = len(flashcards)

    # Ensure index is within the valid range (0 to total_flashcards - 1)
    index = max(0, min(index, total_flashcards - 1))

    # Get the current flashcard based on the index
    current_flashcard = flashcards[index]

    # Calculate the previous and next flashcard indexes
    prev_index = index - 1 if index > 0 else 0
    next_index = index + 1 if index < total_flashcards - 1 else total_flashcards - 1

    # Render the flashcards page with the current flashcard, navigation, and total flashcards
    return render_template('flashcards.html', flashcard=current_flashcard,
                           prev_index=prev_index, next_index=next_index,
                           total_flashcards=total_flashcards, index=index)

# Admin route - Add new flashcards
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':  # Check if user is admin
        return redirect(url_for('flashcards'))  # Non-admin users are redirected

    # The rest of the admin logic goes here
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        if not question or not answer:
            flash("Question and Answer cannot be empty.", "error")
            return render_template('admin.html')

        # Insert flashcard into the database
        new_flashcard = Flashcard(question=question, answer=answer)
        db.session.add(new_flashcard)
        db.session.commit()

        flash('Flashcard added successfully!', 'success')
        return redirect(url_for('admin'))  # Reload admin page

    return render_template('admin.html')

# Login route - Displays the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.get(username)
        if user and user.check_password(password):  # Authenticate user
            login_user(user)
            return redirect(url_for('flashcards'))  # Redirect to flashcards page after login
        else:
            flash("Invalid credentials, please try again.", "error")
    
    return render_template('login.html')

# Logout route - Ends the session
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Main entry point for running the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
