import jwt


def generate_token(payload):
    encoded = jwt.encode(payload, "secret", algorithm="HS256")
    return encoded


def decoded_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        return {"err": False, "payload": decoded, "message": "decoded success"}
    except jwt.exceptions.DecodeError:
        return {"err": True, "payload": None, "message": "error with supplied token"}
    except jwt.exceptions.InvalidTokenError:
        return {"err": True, "payload": None, "message": "supplied token is invalid"}
    except Exception as e:
        return {"err": True, "payload": None, "message": str(e)}
