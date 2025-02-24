from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker,Session

# DB credentials
username = 'root'
password = '80eKae!?'
host = 'localhost'
dbname = 'device_tracker'

# Create the database connection
DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}/{dbname}"

# Create an engine to connect to MySQL
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with Session(engine) as session:
        result = session.execute(text("SELECT 1"))
        print("Connected Successfully:", result.scalar())
except Exception as e:
    print("Connection Failed:", e)

# # Function to get a session
# def get_db():
#     db = SessionLocal()  # Open a session
#     try:
#         yield db  # Provide session
#     finally:
#         db.close()  # Close session after use

# def fetch_and_insert():
#     with SessionLocal() as db:  # Open session
#         # ✅ Fetching data
#         result = db.execute("SELECT * FROM your_table")
#         for row in result:
#             print(row)
#
#         # ✅ Inserting new data
#         db.execute("INSERT INTO your_table (column1) VALUES ('NewValue')")
#         db.commit()  # Commit the transaction
#
# fetch_and_insert()  # Runs everything
