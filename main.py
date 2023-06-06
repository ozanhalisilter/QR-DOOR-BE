from fastapi import FastAPI
import pyotp

app = FastAPI()

@app.get('/otp/{user_id}')
def Generate_OTP(user_id: str):
    totp = pyotp.TOTP(user_id)
    return user_id+"_"+totp.now()


@app.get('/validate/{string}')
def Validate_OTP(string:str):
    user_id = string.split("_")[0]
    otp = string.split("_")[1]

    totp = pyotp.TOTP(user_id)

    return user_id+"_"+totp.now() == user_id+"_"+otp
