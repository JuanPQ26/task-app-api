import os
# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# dotenv
import dotenv

# init .env file
dotenv.load_dotenv()

# database credentials
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

# validate database credentials
if db_host is None:
    raise Exception("No proporciono el host de la base de datos")
if db_name is None:
    raise Exception("No proporciono el nombre de la base de datos")
if db_user is None:
    raise Exception("No proporciono el usuario de la base de datos")
if db_pass is None:
    raise Exception("No proporciono la contraseña de la base de datos")

# database connection string
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
