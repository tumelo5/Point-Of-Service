from sqlalchemy import Column, Integer, String, text, ForeignKey, DDL
from sqlalchemy.orm import relationship
from sqlalchemy.event import listen

from my_project.models.employees_model import Base
from my_project.database.database import engine



#        CLIENTS TABLE
# -----------------------------
class Client(Base):
    """Stores all client names (e.g., companies that own devices)"""
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(50), unique=True, nullable=False)

    # One-to-many relationship with POSDevice
    devices = relationship("POSDevice", back_populates="client")



#         MODELS TABLE
# -----------------------------
class POSModel(Base):
    """Stores all unique POS device models"""
    __tablename__ = "pos_models"

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(50), unique=True, nullable=False)

    # One-to-many relationship with POSDevice
    devices = relationship("POSDevice", back_populates="model")



#      DEVICES TABLE
# -----------------------------
class POSDevice(Base):
    """Stores detailed information about POS devices"""
    __tablename__ = "pos_devices"

    device_id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    serial_prefix = Column(String(30), nullable=False)

    # Original CSV values (raw input)
    model_name = Column(String(50), nullable=False)
    client_name = Column(String(50), nullable=False)

    # Foreign Keys
    model_id = Column(Integer, ForeignKey("pos_models.model_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)

    # Relationships
    model = relationship("POSModel", back_populates="devices")
    client = relationship("Client", back_populates="devices")
    technician_work = relationship("TechnicianWork", back_populates="device")



#     PARTS TABLES (BY MODEL)  #

# Each class below represents a different POS model's parts inventory

class N910stdPart(Base):
    __tablename__ = "n910std_parts"
    part_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    part_name = Column(String(255), nullable=False)
    part_number = Column(String(255), nullable=False)
    faults = Column(String(225), nullable=False)


class N910ProPart(Base):
    __tablename__ = "n910pro_parts"
    part_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    part_name = Column(String(255), nullable=False)
    part_number = Column(String(255), nullable=False)
    faults = Column(String(255), nullable=False)


class Move3000Part(Base):
    __tablename__ = "move3000_parts"
    part_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), nullable=False)
    faults = Column(String(50), nullable=False)


class Move2500Part(Base):
    __tablename__ = "move2500_parts"
    part_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), nullable=False)
    faults = Column(String(50), nullable=False)


class IWL250Part(Base):
    __tablename__ = "iwl250_parts"
    part_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), nullable=False)
    faults = Column(String(50), nullable=False)


class Link2000Part(Base):
    __tablename__ = "link2000_parts"
    part_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), nullable=False)
    faults = Column(String(50), nullable=False)



#     AUTO-INCREMENT SETUP

# Default starting values for each table's AUTO_INCREMENT
auto_increment_statements = {
    "clients": 1000,
    "pos_models": 2000,
    "pos_devices": 3000,
    "n910std_parts": 4000,
    "n910pro_parts": 5000,
    "move3000_parts": 6000,
    "move2500_parts": 7000,
    "iwl250_parts": 8000,
    "link2000_parts": 9000,
}

# SQLAlchemy event listener to set custom AUTO_INCREMENT values on table creation
def set_auto_increment(target, connection, **kw):
    for table, value in auto_increment_statements.items():
        sql = text(f"ALTER TABLE {table} AUTO_INCREMENT = {value}")
        connection.execute(sql)

# Register event listener
listen(Base.metadata, "after_create", set_auto_increment)

# Create all tables
Base.metadata.create_all(engine)
