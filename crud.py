import os
import logging
import pandas as pd
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker
from my_project.models import employees_model, client_model
from my_project.models.client_model import POSDevice, POSModel, Client
from my_project.database.database import engine, SessionLocal

# Configure logging with INFO level and timestamp
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get base directory of the current script for relative CSV file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# List of tuples containing (CSV file path, ORM model, unique ID field, optional unique field)
csv_model_pairs = [
    # Uncomment and add more if needed
    # (os.path.join(BASE_DIR, "data", "employees.csv"), employees_model.CompanyEmployeeInfo, "emp_id", "emp_name"),
    (os.path.join(BASE_DIR, "data", "clients.csv"), client_model.Client, "client_id", None),
    # (os.path.join(BASE_DIR, "data", "pos_models.csv"), client_model.POSModel, "model_id", None),

    (os.path.join(BASE_DIR, "data", "iwl250 parts.csv"), client_model.IWL250Part, "part_id", None),
    (os.path.join(BASE_DIR, "data", "link2000 parts.csv"), client_model.Link2000Part, "part_id", None),
    (os.path.join(BASE_DIR, "data", "move2500 parts.csv"), client_model.Move2500Part, "part_id", None),
    (os.path.join(BASE_DIR, "data", "move3000 parts.csv"), client_model.Move3000Part, "part_id", None),
    (os.path.join(BASE_DIR, "data", "n910pro parts.csv"), client_model.N910ProPart, "part_id", None),
    (os.path.join(BASE_DIR, "data", "n910std parts.csv"), client_model.N910stdPart, "part_id", None),
]

# Cache to store existing IDs per table to avoid repeated DB queries
existing_ids_cache = {}

# Cache to store existing employee names (special case)
existing_employee_names = set()

def load_existing_ids(db, model, id_field):
    """Load existing unique IDs from the DB for a given model to prevent duplicates."""
    try:
        # Query returns list of tuples like [(id1,), (id2,), ...]
        existing_ids = db.query(getattr(model, id_field)).all()
        # Extract first element from each tuple to get IDs as a set
        return {record[0] for record in existing_ids}
    except Exception as e:
        logging.error(f"❌ Error loading existing IDs for {model.__tablename__}: {e}")
        return set()

def load_existing_employee_names(db):
    """Load all existing employee names from the employees table."""
    try:
        names = db.query(employees_model.CompanyEmployeeInfo.emp_name).all()
        return {record[0] for record in names}
    except Exception as e:
        logging.error(f"❌ Error loading employee names: {e}")
        return set()

def insert_csv_data(csv_file, model, id_field, unique_field=None):
    """
    Read CSV, filter out existing records, and bulk insert new unique records.
    unique_field is used for special duplicate checks (like employee names).
    """
    if not os.path.exists(csv_file):
        logging.warning(f"⚠️ File not found: {csv_file}")
        return

    try:
        # Load CSV data as strings to avoid datatype issues
        df = pd.read_csv(csv_file, dtype=str)
        # Normalize columns: lowercase & strip spaces
        df.columns = [col.lower().strip() for col in df.columns]
        # Trim string fields to max 255 chars (safe for DB varchar limits)
        df = df.applymap(lambda x: x.strip()[:255] if isinstance(x, str) else x)
        df.fillna(value=pd.NA, inplace=True)  # Convert NaNs to pandas NA

        with SessionLocal() as db:
            # Load existing IDs for this table only once, cache for reuse
            if model.__tablename__ not in existing_ids_cache:
                existing_ids_cache[model.__tablename__] = load_existing_ids(db, model, id_field)

            # Special handling for employees.csv to avoid duplicate emp_name and emp_id
            if csv_file.endswith("employees.csv"):
                global existing_employee_names
                if not existing_employee_names:
                    existing_employee_names = load_existing_employee_names(db)

                # Filter new records where emp_name AND emp_id don't exist
                new_records = [
                    record for record in df.to_dict(orient="records")
                    if record.get("emp_name") not in existing_employee_names
                    and record.get(id_field) not in existing_ids_cache[model.__tablename__]
                ]
                # Update employee names cache with newly added records
                existing_employee_names.update({record.get("emp_name") for record in new_records})
            else:
                # For other CSVs, just check ID uniqueness
                new_records = [
                    record for record in df.to_dict(orient="records")
                    if record.get(id_field) not in existing_ids_cache[model.__tablename__]
                ]

            if new_records:
                # Bulk save ORM model instances created from the records
                db.bulk_save_objects([model(**record) for record in new_records])
                db.commit()
                logging.info(f"✅ Inserted {len(new_records)} records into {model.__tablename__}")
                # Update cache with newly inserted IDs
                existing_ids_cache[model.__tablename__].update(
                    {record.get(id_field) for record in new_records}
                )
            else:
                logging.info(f"No new records to insert into {model.__tablename__}")

    except IntegrityError as e:
        logging.warning(f" IntegrityError while inserting into {model.__tablename__}. Possibly duplicate ID(s). Details: {e}")
    except DataError:
        logging.error(f" Data error in {csv_file}, possibly due to incorrect field formats.")
    except Exception as e:
        logging.error(f" Unexpected error inserting into {model.__tablename__}: {e}")

# Loop through all CSV files and models to insert data
for csv_file, model, id_field, unique_field in csv_model_pairs:
    insert_csv_data(csv_file, model, id_field, unique_field)

logging.info("🎯 Data processing completed successfully!")


# ----------------------------------------------------------------------
# Specific function to insert POSDevice records efficiently in bulk,
# with checks for duplicates and foreign key existence.

# CSV file path for POS devices
csv_file_path = os.path.join(BASE_DIR, "data", "pos_devices.csv")

# Create a session factory bound to the engine
SessionFactory = sessionmaker(bind=engine)

def insert_pos_devices(csv_file):
    """Bulk insert POS devices from CSV, avoid duplicates by serial_number."""
    session = SessionFactory()

    try:
        df = pd.read_csv(csv_file)
        # Drop rows with missing critical foreign key data
        df = df.dropna(subset=["model_name", "client_name"])

        new_devices = []
        batch_size = 5000  # Tune batch size as needed

        for _, row in df.iterrows():
            # Check if a device with the serial number already exists (efficient scalar exists query)
            exists_check = session.query(
                session.query(POSDevice).filter_by(serial_number=row["serial_number"]).exists()
            ).scalar()
            if exists_check:
                continue  # Skip duplicates

            # Fetch related model and client records for foreign keys
            model = session.query(POSModel).filter_by(model_name=row["model_name"]).first()
            client = session.query(Client).filter_by(client_name=row["client_name"]).first()

            # Skip row if foreign keys are invalid/missing
            if not model or not client:
                continue

            # Create POSDevice instance with required fields and foreign keys
            new_device = POSDevice(
                serial_number=row["serial_number"],
                serial_prefix=row.get("serial_prefix"),  # Use get() in case missing
                model_name=row["model_name"],
                client_name=row["client_name"],
                model_id=model.model_id,
                client_id=client.client_id
            )
            new_devices.append(new_device)

            # Commit batch if batch size reached to manage memory & speed
            if len(new_devices) >= batch_size:
                session.bulk_save_objects(new_devices)
                session.commit()
                new_devices.clear()  # Free memory

        # Insert any remaining devices after loop
        if new_devices:
            session.bulk_save_objects(new_devices)
            session.commit()

        logging.info("✅ POS devices data inserted successfully!")

    except IntegrityError as e:
        session.rollback()
        logging.error(f"❌ Integrity error inserting POS devices: {e}")

    except Exception as e:
        logging.error(f"❌ Unexpected error inserting POS devices: {e}")

    finally:
        session.close()

# Run POS devices insertion
insert_pos_devices(csv_file_path)



rename_map = {
    "fnb": "BankOne",
    "sbsa": "Unity Bank",
    "nedbank": "Heritage Bank",
    "absa": "Evergreen Bank"
}


