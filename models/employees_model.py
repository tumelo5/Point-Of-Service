from sqlalchemy import Integer, String, Column, DDL, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.event import listen
from my_project.database.database import engine
from werkzeug.security import generate_password_hash, check_password_hash


# Base class for all models
class Base(DeclarativeBase):
    pass


# Employee table to store company employee details
class CompanyEmployeeInfo(Base):
    __tablename__ = "employee"

    emp_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique employee ID
    full_name = Column(String(50), nullable=False)                  # Full name of employee
    department = Column(String(50), nullable=False)                 # Department they work in
    job_title = Column(String(50), nullable=False)                  # Job title
    status = Column(String(50), default="not available")            # Availability status

    # One-to-many relationship with technician work (defined in TechnicianWork model)
    technician_work = relationship("TechnicianWork", back_populates="employee")


# User table to store login credentials and link to employee
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)     # Unique user ID
    username = Column(String(50), nullable=False, unique=True)          # Unique login name
    password_hash = Column(String(255), nullable=False)                 # Hashed password
    emp_id = Column(Integer, ForeignKey("employee.emp_id"), nullable=False)  # Link to employee

    # Relationship to employee info
    employee = relationship("CompanyEmployeeInfo", backref="user")

    def set_password(self, password):
        """Hashes and sets the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


# Dictionary of starting AUTO_INCREMENT values per table
auto_increment_value = {
    "employee": 1,  # Start employee ID from 1
    "user": 555     # Start user ID from 555
}

# Event function to set custom AUTO_INCREMENT after table creation
def set_auto_increment(target, connection, **kw):
    for table, value in auto_increment_value.items():
        sql = text(f"ALTER TABLE {table} AUTO_INCREMENT = {value}")
        connection.execute(sql)

# Apply the auto-increment settings after tables are created
listen(Base.metadata, "after_create", set_auto_increment)

# Create all tables
Base.metadata.create_all(engine)


