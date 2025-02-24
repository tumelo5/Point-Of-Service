from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import DeclarativeBase
from database import engine


class Base(DeclarativeBase):
    pass

class CompanyEmployeeInfo(Base):
    __tablename__ = "company_employee_info"  # Table name in MySQL
    
    #__abstract__ = True # To prevent Base class creating it's own Table
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50),nullable=False)
    department = Column(String(50), nullable=False)
    job_title = Column(String(50), nullable=False)
    status = Column(String(10),default="not available")






































# # Finance Department
# class Finance(Base):
#     __tablename__ = "finance"
#
#     # ----foreign key to be added here
#
# # Repairs Department
# class Repairs(Base):
#     __tablename__ = "repairs"
#
#     # ----foreign key to be added here
#
# # Qaulity Control Department
# class QualityControl(Base):
#     __tablename__ = "quality_control"
#
#     # ----foreign key to be added here
#
# # Configuration departments per banks.
#  # For Absa
# class Absa(Base):
#     __tablename__ = "absa"
#
#     # ----foreign key to be added here
#
#  # For Standard Bank
# class StandardBank(Base):
#     __tablename__ = "standard_bank"
#
#     # ----foreign key to be added here
#
#     # For FNB
# class FNB(Base):
#     __tablename__ = "fnb"

    # ----foreign key to be added here

# Create the table in MySQL
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Table 'Company_Employee_Info' created successfully!")
