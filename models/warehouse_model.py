from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from my_project.models.employees_model import Base, CompanyEmployeeInfo
from my_project.database.database import engine
from my_project.models.client_model import Client, POSDevice


class WarehouseAgent(Base):
    __tablename__ = "agent_work"

    emp_id = Column(Integer, ForeignKey("employees.emp_id"), primary_key=True)
    serial_number = Column(String(50), nullable=False, index=True)
    device_id = Column(Integer, ForeignKey("pos_devices.device_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    batch_number = Column(String(50), nullable=False)
    sla_deadline = Column(DateTime, nullable=False)
    device_status = Column(String(50), nullable=False)  # Can be randomly generated externally

    # Relationships
    client = relationship(Client, foreign_keys=[client_id])
    device = relationship(POSDevice, foreign_keys=[device_id])
    employee = relationship(CompanyEmployeeInfo, foreign_keys=[emp_id])


# Create table
Base.metadata.create_all(engine)
