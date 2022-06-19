from datetime import time
import os
from typing import Dict

import jwt

jwtSecret = os.environ.get('JWT_SECRET')

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "userId": user_id,
        "expires": time() + 600
    }
    token = jwt.encode(payload, jwtSecret, algorithm='HS256')

    return token

def decodeJWT(token: str) -> dict:
    try:
        decoded = jwt.decode(token, jwtSecret, algorithms=['HS256'])
        return decoded if decoded["expires"] >= time() else None
    except:
        return {}
