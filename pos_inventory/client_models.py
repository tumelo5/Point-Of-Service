from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Relationship
from database import engine



class Base(DeclarativeBase):
    pass


class Clients(Base):
    """Stores all clients"""
    __tablename= "clients"
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(50),unique=True, nullable=False)

    # relationship to devices
    devices = relationship("Device", back_populates="client")

class DeviceTypes(Base):
    """Stores all device types"""
    __tablename__ = "device_types"
    item_type_id = Column(Integer,primary_key=True, autoincrement=True)
    item_type_name = Column(String(50), nullable=False)
    device_code = Column(String(10),unique=True, nullable=False)

    # Relationship to Devices
    devices = relationship("Device", back_populates="device_type")

class Devices(Base):
    """Stores all devices"""
    __tablename__ = "devices"
    serial_number = Column(String(50), unique=True, nullable=False)
    item_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Relationships
    device_type = relationship("DeviceType", back_populates="devices")
    client = relationship("Client", back_populates="devices")

# clients names
clients = ["ABSA", "FNB", "SBSA", "Nedbank"]


device_types = [
    {"N910std": "device---code"},
    {"N910Pro": "device---code"},
    {"Move3000": "device---code"},
    {"Xlink2500": "device---code"},
    {"Move2500": "device---code"},
    {"IWL250": "device---code"}
    ]

devices = [
    "N910std",
    "N910Pro",
    "MOve3000",
    "Xlink2500",
    "Move2500",
    "IWL250"
    ]


# storage table for all devices(in details) and clients
class PosInvetory(Base):
    pass





# Create Tables
Base.metadata.create_all(engine)

# Session Maker
SessionLocal = sessionmaker(bind=engine)