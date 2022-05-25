def execute(func, msg, *arg, **karg):
    """informing user before and after executing function"""
    print(msg, end=" ", flush=True)
    func(*arg, **karg)
    print("Done")


def b64_to_byte(msg: str) -> bytes:
    """encode string to bytes based on base64"""
    import base64

    return base64.b64decode(msg)


def byte_to_b64(cipher: bytes) -> str:
    """decode bytes to string based on base64"""
    import base64

    return base64.b64encode(cipher).decode()


def encode_jwt_token(payload: dict, key: bytes) -> str:
    """encrypt payload to jwt token"""
    import jwt
    import datetime
    from model.app import App

    app = App.get_instance()
    valid_time = datetime.timedelta(days=0, minutes=app.config["JWT_MINUTE_TIME"])

    payload = {
        "exp": datetime.datetime.utcnow() + valid_time,
        "iat": datetime.datetime.utcnow(),
        "sub": payload,
    }
    return jwt.encode(payload, key, algorithm="HS256")


def decode_jwt_token(token: str, key: bytes) -> dict:
    """decrypt payload from token"""
    import jwt

    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        return {"code": 200, "resp": payload["sub"]}
    except jwt.ExpiredSignatureError as e:
        return {"code": 401, "resp": e}
    except jwt.InvalidTokenError as e:
        return {"code": 401, "resp": e}


def hash_pwd(pwd: str) -> str:
    """hash user password with 16 rounds salt
    Output is hashed bytes encoded using base 64
    """
    import bcrypt

    salt = bcrypt.gensalt(rounds=16)
    hashed = bcrypt.hashpw(pwd.encode(), salt)
    return byte_to_b64(hashed)


def is_correct_pwd(pwd: str, hashed: str) -> bool:
    """validate password with corresponding hashed function"""
    import bcrypt

    hash_value = b64_to_byte(hashed)
    return bcrypt.checkpw(pwd.encode(), hash_value)
