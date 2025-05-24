from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, DDL, event
from sqlalchemy.orm import relationship, sessionmaker, Session
from my_project.models.employees_model import Base
from my_project.database.database import engine
from my_project.models import warehouse_model  # required for relationships
from sqlalchemy.event import listen


class Finance(Base):
    __tablename__ = "finance"

    # Foreign key to employee table; also serves as primary key
    emp_id = Column(Integer, ForeignKey("employees.emp_id"), primary_key=True)

    # Employee name; should be filled from the employees table manually
    financee = Column(String(50), nullable=False)

    serial_number = Column(String(50), nullable=False, index=True)  # Indexed for faster lookup
    batch_number = Column(String(50), nullable=False)

    device_id = Column(Integer, ForeignKey("pos_devices.device_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)

    # Automatically set the current timestamp when the record is created
    date_logged = Column(DateTime, default=func.now())

    # Relationships to referenced tables
    client = relationship("clients", foreign_keys=[client_id])
    device = relationship("POSDevice", back_populates="finance")
    employee = relationship("employees", foreign_keys=[emp_id])


# Starting value for auto-incrementing records
auto_increment_value = 6000

# DDL event to apply custom AUTO_INCREMENT starting value after table creation
def set_auto_increment(target, connection, **kw):
    connection.execute(f"ALTER TABLE {target.name} AUTO_INCREMENT = {auto_increment_value}")

# Attach the DDL event to the Finance table creation event
listen(Finance.__table__, "after_create", set_auto_increment)

# Create all tables in the Base metadata
Base.metadata.create_all(engine)

