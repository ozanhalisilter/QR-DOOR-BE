from fastapi import FastAPI
import pyotp
import base64
from datetime import datetime

app = FastAPI()

# Logs
logs = {}

def generate_otp(user_id: str) -> str:
    user_id_base32 = base64.b32encode(user_id.encode()).decode()
    totp = pyotp.TOTP(user_id_base32)
    otp = f"{user_id_base32}_{totp.now()}"
    
    # Log the operation
    logs[user_id] = {"timestamp": datetime.now(), "validation": None}
    
    return otp

def validate_otp(string: str) -> bool:
    user_id_base32, otp = string.split("_")
    totp = pyotp.TOTP(user_id_base32)
    valid = totp.verify(otp)

    # Find user_id from base32 representation
    user_id = base64.b32decode(user_id_base32.encode()).decode()

    # Log the operation
    if user_id in logs:
        logs[user_id]["validation"] = valid
        logs[user_id]["timestamp"] = datetime.now()

    return valid

@app.get('/otp/{user_id}')
def generate_otp_endpoint(user_id: str):
    otp = generate_otp(user_id)
    return {"qr_string": otp}

@app.get('/validate/{string}')
def validate_otp_endpoint(string: str):
    is_valid = validate_otp(string)
    return {"validation": is_valid}

@app.get('/isvalid/{user_id}')
def is_valid_endpoint(user_id: str):
    if user_id in logs:
        return {"user_id": user_id, "validation": logs[user_id]["validation"]}
    else:
        return {"error": "User ID not found"}
    

@app.get('/logs')
def get_logs():
    return logs