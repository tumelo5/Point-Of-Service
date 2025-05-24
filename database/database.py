from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from my_project.config import username, password, host, dbname

# Construct the database URL for MySQL using the config credentials
DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}/{dbname}"

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Number of connections to keep in the pool
    max_overflow=20      # Additional connections allowed beyond pool_size
)

# Session factory to create DB sessions (manual commit/flush handling)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Test connection by executing a simple SELECT statement
try:
    with SessionLocal() as session:
        result = session.execute(text("SELECT 1"))  # Simple query to test DB connection
        print("Connected Successfully:", result.scalar())  # Should print 1
except Exception as e:
    print("Connection Failed:", e)  # Handle and display connection errors
