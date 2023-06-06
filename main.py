from fastapi import FastAPI
import pyotp
import base64

app = FastAPI()

def generate_otp(user_id: str) -> str:
    user_id_base32 = base64.b32encode(user_id.encode()).decode()
    totp = pyotp.TOTP(user_id_base32)
    return f"{user_id_base32}_{totp.now()}"

def validate_otp(string: str) -> bool:
    user_id_base32, otp = string.split("_")
    user_id = base64.b32decode(user_id_base32).decode()
    totp = pyotp.TOTP(user_id_base32)
    return string == f"{user_id_base32}_{otp}" and totp.verify(otp)

@app.get('/otp/{user_id}')
def generate_otp_endpoint(user_id: str):
    otp = generate_otp(user_id)
    return {"qr_string": otp}

@app.get('/validate/{string}')
def validate_otp_endpoint(string: str):
    is_valid = validate_otp(string)
    return {"validation": is_valid}