from fastapi import FastAPI
import pyotp
import base64

app = FastAPI()

@app.get('/otp/{user_id}')
def Generate_OTP(user_id: str):
    encoded_user_id = base64.b32encode(user_id)
    totp = pyotp.TOTP(encoded_user_id)
    return user_id+"_"+totp.now()

@app.get('/{string}}')
def test(string: str):
    return string

@app.get('/validate/{string}')
def Validate_OTP(string:str):
    user_id = base64.b32decode(string.split("_")[0])
    otp = string.split("_")[1]

    totp = pyotp.TOTP(user_id)

    return user_id+"_"+totp.now() == user_id+"_"+otp
