from fastapi import FastAPI, BackgroundTasks
import pyotp
import base64
from datetime import datetime, timedelta
import time

app = FastAPI()

# Logs
logs = {}

def generate_otp(user_id: str) -> str:
    user_id_base32 = base64.b32encode(user_id.encode()).decode()
    totp = pyotp.TOTP(user_id_base32)
    otp = f"{user_id_base32}_{totp.now()}"
    
    return otp

def validate_otp(string: str) -> bool:
    user_id_base32, otp = string.split("_")
    totp = pyotp.TOTP(user_id_base32)
    valid = totp.verify(otp)

    # Find user_id from base32 representation
    user_id = base64.b32decode(user_id_base32.encode()).decode()

    # Log the operation
    logs[user_id] = {"validation":valid}

    return valid

def reset_user_id(user_id: str):
    time.sleep(30)  # wait 30 seconds
    if user_id in logs:
        logs[user_id]["validation"] = False  # reset the validation for the user_id

@app.get('/otp/{user_id}')
def generate_otp_endpoint(user_id: str, background_tasks: BackgroundTasks):
    otp = generate_otp(user_id)
    return {"qr_string": otp}

@app.get('/validate/{string}')
def validate_otp_endpoint(string: str, background_tasks: BackgroundTasks):
    is_valid = validate_otp(string)
    user_id_base32 = string.split("_")[0]
    user_id = base64.b32decode(user_id_base32.encode()).decode()
    background_tasks.add_task(reset_user_id, user_id)  # schedule the user_id to be reset in 30 seconds
    return {"validation": is_valid}

@app.get('/isvalid/{user_id}')
def is_valid_endpoint(user_id: str):
    if user_id in logs:
        return {"user_id": user_id, "validation": logs[user_id]["validation"]}
    else:
        return {"user_id": user_id, "validation": False}

    

@app.get('/logs')
def get_logs():
    return logs