from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from database.db import (get_db, init_db, seed_db, find_user_by_email,
                          create_user, verify_user_login,
                          get_user_by_id, get_expenses_by_user_and_date_range)

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Full name is required.")

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    if find_user_by_email(email):
        return render_template("register.html", error="An account with that email already exists.")

    create_user(name, email, password)
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route — handles both GET (show form) and POST (process login).
    
    GET: Display login form
    POST: Validate credentials and create session
    """
    if request.method == "GET":
        return render_template("login.html")
    
    # POST: Handle form submission
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    
    # Validate inputs
    if not email or not password:
        return render_template("login.html", error="Email and password are required.")
    
    # Verify credentials
    user = verify_user_login(email, password)
    
    if not user:
        # Generic error message — don't reveal if email exists or not
        return render_template("login.html", error="Invalid email or password.")
    
    # Create session
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    session['user_email'] = user['email']
    
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route("/logout")
def logout():
    """
    Logout route — clear session and redirect to landing page.
    """
    session.clear()
    return redirect(url_for('landing'))


@app.route("/dashboard")
def dashboard():
    """
    Dashboard route — displays user's expense summary.
    Protected: redirects to login if user not authenticated.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_name = session.get('user_name', 'User')
    return render_template("dashboard.html", user_name=user_name)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])

    from_date = request.args.get('from_date', '').strip()
    to_date   = request.args.get('to_date', '').strip()

    expenses     = []
    total_amount = 0.0
    error        = None
    filtered     = False

    if from_date or to_date:
        if not from_date or not to_date:
            error = "Both From and To dates are required."
        else:
            try:
                d_from = datetime.strptime(from_date, "%Y-%m-%d")
                d_to   = datetime.strptime(to_date,   "%Y-%m-%d")
                if d_from > d_to:
                    error = "From date must not be after To date."
                else:
                    expenses     = get_expenses_by_user_and_date_range(
                                       session['user_id'], from_date, to_date)
                    total_amount = sum(e['amount'] for e in expenses)
                    filtered     = True
            except ValueError:
                error = "Invalid date format. Use YYYY-MM-DD."

    return render_template("profile.html",
        user=user,
        expenses=expenses,
        total_amount=total_amount,
        from_date=from_date,
        to_date=to_date,
        filtered=filtered,
        error=error,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
