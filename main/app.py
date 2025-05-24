from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session as flask_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import Session
import string
import random

# Local imports: forms for user input, database engine, models for ORM, and configuration
from my_project.forms import SignupForm, LoginForm, TechnicianWorkForm, WarehouseAgentForm
from my_project.database.database import engine
from my_project.models.employees_model import CompanyEmployeeInfo, User
from my_project.models.client_model import POSDevice, N910stdPart, N910ProPart, IWL250Part, Move2500Part, Move3000Part, Link2000Part
from my_project.models.repairs_model import Fault
from my_project.config import Config

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from Config class
app.config['TEMPLATES_AUTO_RELOAD'] = True # Enable auto-reload of templates on change
app.jinja_env.cache = {}   # Disable Jinja template caching for development


# Password validation function: checks for length, uppercase, lowercase, digit, and special character
def is_valid_password(password):
    return (
        len(password) >= 8 and
        any(c.isupper() for c in password) and
        any(c.islower() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in string.punctuation for c in password)
    )


# --- Routes ---

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Handle user signup with validation and linking to employee records
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        with Session(engine) as session:
            # Check if the username corresponds to an existing employee (case-insensitive, trimmed)
            employee = session.query(CompanyEmployeeInfo).filter(
                func.lower(func.trim(CompanyEmployeeInfo.full_name)) == username.strip().lower()
            ).first()
            if not employee:
                flash("Error: Username not found.", "danger")
                return redirect(url_for("signup"))

            # Prevent duplicate user registration
            if session.query(User).filter_by(username=username).first():
                flash("Error: User already registered.", "danger")
                return redirect(url_for("signup"))

            # Create new user linked to employee and hash the password securely
            new_user = User(username=username, emp_id=employee.emp_id)
            new_user.set_password(password)
            session.add(new_user)
            session.commit()

            flash("User registered successfully!", "success")
            return redirect(url_for("login"))

    # Render signup page with the form
    return render_template("auth.html", form=form, page_title="Sign Up", button_text="Sign Up")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login, check credentials, and set session
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            with Session(engine) as db_session:
                user = db_session.query(User).filter_by(username=username).first()
                # Check password and set username in Flask session if valid
                if user and user.check_password(password):
                    flask_session["username"] = user.username
                    flash("Successful login!", "success")
                    return redirect(url_for("dashboard"))
                else:
                    flash("Invalid username or password", "danger")
        except Exception as e:
            print(f"Login error: {e}")
            flash("An error occurred during login", "danger")

    # Render login page with form
    return render_template("auth.html", form=form, page_title="Login", button_text="Login")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    username = flask_session.get("username")
    if not username:
        # Redirect to login if user is not authenticated
        return redirect(url_for("login"))

    form = TechnicianWorkForm()
    with Session(engine) as db_session:
        user = db_session.query(User).filter_by(username=username).first()
        faults = db_session.query(Fault).all()
        # Populate fault choices dynamically for form dropdown
        form.fault_id.choices = [(fault.fault_id, fault.fault_name) for fault in faults]

        if user and user.employee:
            employee = user.employee
            department = employee.department
            emp_id = employee.emp_id

            # Different dashboard behavior depending on employee department
            if department == "Repairs":
                # Process technician work form submission
                if form.validate_on_submit():
                    new_entry = TechnicianWork(
                        emp_id=emp_id,
                        tech_name=employee.full_name,
                        serial_number=form.serial_number.data,
                        batch_number=form.batch_number.data,
                        sla_deadline=form.sla_deadline.data,
                        device_id=form.device_id.data,
                        client_id=form.client_id.data,
                        fault_id=form.fault_id.data,
                        status_id=form.status_id.data,
                    )
                    db_session.add(new_entry)
                    db_session.commit()
                    flash("Repair record submitted.", "success")
                return render_template("repairs_dashboard.html", form=form, name=employee.full_name)

            elif department == "Warehouse":
                # Warehouse dashboard uses a different form and submission logic
                form = WarehouseAgentForm()
                if form.validate_on_submit():
                    warehouse_entry = Warehouse(
                        emp_id=emp_id,
                        warehouse_agent=employee.full_name,
                        serial_number=form.serial_number.data,
                        batch_number=form.batch_number.data,
                        client_id=form.client_id.data,
                        device_id=form.device_id.data,
                        sla_deadline=form.sla_deadline.data,
                        device_status=form.device_status.data  # selected status
                    )
                    db_session.add(warehouse_entry)
                    db_session.commit()
                    flash("Warehouse entry submitted.", "success")
                return render_template("warehouse_dashboard.html", form=form, name=employee.full_name)

            else:
                # Default dashboard view for other departments, no form
                return render_template("dashboard.html", name=employee.full_name, form=None)

        # If no employee linked to user, show error and redirect to login
        flash("Employee not found.", "danger")
        return redirect(url_for("login"))


@app.route('/get-info-by-serial/<serial>')
def get_info_by_serial(serial):
    # API endpoint to return device and client info by serial number in JSON format
    try:
        with Session(engine) as session:
            device = session.query(POSDevice).filter_by(serial_number=serial).first()
            if device:
                return jsonify({
                    "device": device.model_name,
                    "client": device.client_name
                })
            # Return None values if device not found
            return jsonify({"device": None, "client": None})
    except Exception as e:
        print(f"Error fetching device info: {e}")
        # Return None on errors as well to avoid client-side crashes
        return jsonify({"device": None, "client": None})


# --- Fault/Parts logic ---

# Mapping of serial number prefixes to the correct parts model
PART_TABLES = [
    ("NS45", N910stdPart),
    ("NP47", N910ProPart),
    ("3000", Move3000Part),
    ("2500", Move2500Part),
    ("2000", Link2000Part),
    ("IWL",IWL250Part)
    # Add more as needed, with longer prefixes first to ensure correct matching
]

@app.route("/get_faults_by_serial_number", methods=["POST"])
def get_faults_by_serial_number():
    # Accept serial number in JSON, find the corresponding parts and faults
    data = request.get_json()
    serial_number = data.get("serial_number")
    prefix = serial_number[:4] # First try 4-char prefix

    # Find matching parts table by prefix (try 4-char, then 3-char)
    part_model = next((model for pfx, model in PART_TABLES if prefix.startswith(pfx)), None)
    if not part_model:
        prefix = serial_number[:3]
        part_model = next((model for pfx, model in PART_TABLES if prefix.startswith(pfx)), None)

    if not part_model:
        # No matching part model found, return 404 error
        return jsonify({"error": "No matching part model for serial number"}), 404

    with Session(engine) as db_session:
        results = db_session.query(part_model).all()
        if not results:
            # No parts found for this model
            return jsonify({"error": "No parts found for this serial number"}), 404

        # Return list of faults and their associated part numbers
        fault_part_pairs = [{"fault": part.faults, "part_number": part.part_number} for part in results]
        return jsonify(fault_part_pairs)


@app.route("/get_part_number", methods=["POST"])
def get_part_number():
    # Given a fault and serial number, find the associated part number
    data = request.get_json()
    fault = data.get("fault")
    serial_number = data.get("serial_number")

    # Validate input presence
    if not fault or not serial_number:
        return jsonify({"error": "Missing fault or serial number"}), 400

    # Determine which part model to query based on serial prefix
    prefix = serial_number[:4]
    part_model = next((model for pfx, model in PART_TABLES if prefix.startswith(pfx)), None)
    if not part_model:
        prefix = serial_number[:3]
        part_model = next((model for pfx, model in PART_TABLES if prefix.startswith(pfx)), None)

    if not part_model:
        return jsonify({"error": "No matching part model for serial number"}), 404

    with Session(engine) as db_session:
        # Query part by fault name
        part = db_session.query(part_model).filter(part_model.faults == fault).first()
        if not part:
            return jsonify({"error": "No part found for the given fault"}), 404

        # Return the fault and part number as JSON
        return jsonify({"fault": part.faults, "part_number": part.part_number})

# --- Run the Flask app ---
if __name__ == "__main__":
    app.run(debug=True)

