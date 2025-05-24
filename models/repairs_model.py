from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, DDL, ForeignKey, text
from my_project.models.employees_model import Base
from my_project.database.database import engine
from my_project.models.client_model import Client
from my_project.models.employees_model import CompanyEmployeeInfo
from sqlalchemy.event import listen


# Fault table: Represents faults linked to specific parts
class Fault(Base):
    __tablename__ = "faults"

    fault_id = Column(Integer, primary_key=True, autoincrement=True)
    fault_name = Column(String(100), nullable=False)

    # One-to-One relationship with Part
    part_number = Column(String(50), ForeignKey("parts.part_number"), nullable=False)
    part = relationship("Part", back_populates="fault", uselist=False)


# Part table: Represents parts, each can be linked to one fault
class Part(Base):
    __tablename__ = "parts"

    part_id = Column(Integer, primary_key=True, autoincrement=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), nullable=False)

    # One-to-One relationship back to Fault
    fault = relationship("Fault", back_populates="part", uselist=False)


# Status table: Represents status labels for devices
class Status(Base):
    __tablename__ = "statuses"

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(20), unique=True, nullable=False)


# TechnicianWork table: Tracks work done by technicians on devices
class TechnicianWork(Base):
    __tablename__ = "technician_work"

    tech_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(Integer, ForeignKey("employee.emp_id"), nullable=False)
    serial_number = Column(String(50), nullable=False, index=True)  # Scanned by technician
    batch_number = Column(String(50), nullable=False)
    date_logged = Column(DateTime, default=func.now())  # Timestamp for when entry is logged
    sla_deadline = Column(DateTime, nullable=False)  # Deadline for SLA
    device_id = Column(Integer, ForeignKey("pos_devices.device_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    fault_id = Column(Integer, ForeignKey("faults.fault_id"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.status_id"), nullable=False, default="Pending")

    # Relationships to foreign tables
    fault = relationship("Fault", foreign_keys=[fault_id])
    client = relationship("Client", foreign_keys=[client_id])
    device = relationship("POSDevice", back_populates="technician_work")
    employee = relationship("CompanyEmployeeInfo", foreign_keys=[emp_id])
    status = relationship("Status")


# Dictionary of tables and their respective AUTO_INCREMENT starting values
tables_auto_increment = {
    'faults': 1000,
    'parts': 100,
    'statuses': 10000
    # Add more table values here as needed
}


# DDL trigger to set custom AUTO_INCREMENT values after table creation
def set_auto_increment(target, connection, **kwargs):
    for table in target.tables.values():
        table_name = table.name
        if table_name in tables_auto_increment:
            increment_value = tables_auto_increment[table_name]
            connection.execute(text(f"ALTER TABLE {table_name} AUTO_INCREMENT = {increment_value};"))


# Attach listener to apply AUTO_INCREMENT settings after schema creation
listen(Base.metadata, 'after_create', set_auto_increment)

# Create all tables
Base.metadata.create_all(engine)




