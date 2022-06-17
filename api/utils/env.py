import os
import dotenv

# load .env file
dotenv.load_dotenv()


def getenv(key, default=None):
    return os.getenv(key, default=default)
