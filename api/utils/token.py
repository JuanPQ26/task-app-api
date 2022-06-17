import jwt
# utils
from api.utils import env


def generate_token(payload):
    encoded = jwt.encode(payload, env.getenv("API_SECRET", ""), algorithm="HS256")
    return encoded


def decoded_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, env.getenv("API_SECRET", ""), algorithms=["HS256"])
        return {"err": False, "payload": decoded, "message": "decoded success"}
    except jwt.exceptions.DecodeError:
        return {"err": True, "payload": None, "message": "error with supplied token"}
    except jwt.exceptions.InvalidTokenError:
        return {"err": True, "payload": None, "message": "supplied token is invalid"}
    except Exception as e:
        return {"err": True, "payload": None, "message": str(e)}
