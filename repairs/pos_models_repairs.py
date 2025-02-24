from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from database import engine



class Base(DeclarativeBase):
    pass

# pos models
class Pos_models(Base):
    __tablename__ = "pos_models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(50),unique=True, nullable=False) # double check if a relationship can be estalbised
    # so that the devices can be retieved from the PosInventory, if is doable,
    # rename "model_name" to something relevant



# faults
class Faults(Base):
    __tablename__ = "faults"
    fault_id = Column(Integer, autoincrement=True)
    fault_name = Column(String(50))


# parts
class Parts(Base):
    __tablename__ = "parts"
    part_id = Column(Integer, autoincrement=True)
    part_name = Column(String(50), nullable=False)
    part_number = Column(String(50), nullable=False)


pos_models = [
    "Move3500", "Move2500", "IWL250", "Link3000",
    "N910std", "N910Pro", "SP930", "SP630"
    "Dax8000", "Lane3000"] # to be reconsidered as the modelas are stored in the inventory,
    # a relationship could be created

faults = [
    "lower casing damaged",
    "upper casing damaged",
    "battery door damaged",
    "printer cover damaged",
    "battery damanged",
    "internal battery(cmos) low",
    "printer faulty",
    "charging por/USB faulty"
    ]

parts = [] # to be replanned as to whether dictionaries should be used, where fault is matched with a part
            #....dictionary within a dictionary