from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length

# Signup form for new user registration
class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)]  # Username required, length between 3 and 50 chars
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]  # Password is required
    )
    submit = SubmitField("Sign Up")  # Submit button for signup

# Login form for existing users
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]  # Username required
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]  # Password required
    )
    submit = SubmitField("Login")  # Submit button for login

# Form for technicians to log work on devices
class TechnicianWorkForm(FlaskForm):
    emp_id = IntegerField(
        "Employee ID",
        validators=[DataRequired()]  # Employee ID must be provided and integer
    )
    serial_number = StringField(
        "Serial Number",
        validators=[DataRequired()]  # Serial number is required
    )
    batch_number = StringField(
        "Batch Number",
        validators=[DataRequired()]  # Batch number is required
    )
    sla_deadline = DateTimeField(
        "SLA Deadline",
        format="%Y-%m-%d %H:%M:%S",  # Expected datetime format
        validators=[DataRequired()]  # SLA deadline is required
    )
    device_id = SelectField(
        "Device",
        coerce=int,  # Coerce selected value to int for IDs
        validators=[DataRequired()]  # Must select a device
    )
    client_id = SelectField(
        "Client",
        coerce=int,  # Coerce selected client ID to int
        validators=[DataRequired()]  # Client selection required
    )
    fault_id = SelectField(
        "Fault",
        choices=[],  # Initially empty, to be populated dynamically, e.g. from DB
        coerce=int  # Coerce selected fault ID to int
    )
    status_id = SelectField(
        "Status",
        coerce=int,  # Coerce selected status ID to int
        validators=[DataRequired()]  # Status must be selected
    )
    submit = SubmitField("Submit")  # Submit button for the form


class WarehouseAgentForm(FlaskForm):
    emp_id = SelectField(
        "Employee",
        coerce=int,  # Coerce selected employee ID to int
        validators=[DataRequired()]  # Employee selection required
    )
    serial_number = StringField(
        "Serial Number",
        validators=[DataRequired()]  # Serial number is required
    )
    batch_number = StringField(
        "Batch Number",
        validators=[DataRequired()]  # Batch number is required
    )
    sla_deadline = DateTimeField(
        "SLA Deadline",
        format="%Y-%m-%d %H:%M:%S",  # Expected datetime format
        validators=[DataRequired()]  # SLA deadline is required
    )
    device_id = SelectField(
        "Device",
        coerce=int,  # Coerce selected value to int for IDs
        validators=[DataRequired()]  # Must select a device
    )
    client_id = SelectField(
        "Client",
        coerce=int,  # Coerce selected client ID to int
        validators=[DataRequired()]  # Client selection required
    )
    device_status = SelectField(
        'Device Status',
        choices=[('Received', 'Received'), ('In Query', 'In Query')],
        validators=[DataRequired()]
    ) # Device status is required

    submit = SubmitField("Submit")  # Submit button for the form