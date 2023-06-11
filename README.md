# QR-DOOR-BACKEND - OTP Verification API with FastAPI

## Introduction

Our project is an OTP (One-Time Password) verification API built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.

The API allows users to generate OTPs and validate them. It provides a secure and convenient way to authenticate users for various applications, such as two-factor authentication (2FA) and passwordless login.

## Features

1. OTP Generation: Users can generate OTPs by providing their user ID. The API uses the PyOTP library to generate time-based OTPs (TOTP).
2. OTP Validation: Users can validate OTPs by providing a string that includes the user ID and OTP. The API verifies the OTP's validity and logs the validation result.
3. Background Task: Upon successful validation, the API schedules a background task to reset the validation status for the user ID after a certain period (30 seconds in this case). This provides an added layer of security by automatically expiring the OTP validity.

## API Endpoints

The API exposes the following endpoints:

1. `GET /otp/{user_id}`:
   - Generates an OTP for the specified `user_id`.
   - Returns a JSON response containing the OTP in the form of a QR string.
   - Example response:
     ```
     {
       "qr_string": "<user_id_base32>_<generated_otp>"
     }
     ```

2. `GET /validate/{string}`:
   - Validates the OTP specified in the `string` parameter.
   - Schedules a background task to reset the validation status for the user ID after 30 seconds.
   - Returns a JSON response indicating the validation result.
   - Example response:
     ```
     {
       "validation": true
     }
     ```

3. `GET /isvalid/{user_id}`:
   - Checks if the specified `user_id` has a valid OTP validation record.
   - Returns a JSON response indicating the validation status for the user ID.
   - Example response:
     ```
     {
       "user_id": "<user_id>",
       "validation": true
     }
     ```

4. `GET /logs`:
   - Retrieves the current logs of OTP validations.
   - Returns a JSON response containing the logs.
   - Example response:
     ```
     {
       "<user_id>": {
         "validation": true
       },
       ...
     }
     ```

## Swagger Documentation

We have integrated Swagger UI with our API for easy exploration and testing. Swagger UI provides an interactive interface to interact with the API endpoints and visualize the request and response details.

To access the Swagger documentation and explore our API, please visit the following URL:

[Swagger Documentation](https://your-api-base-url/docs)

## Conclusion

Our OTP verification API built with FastAPI offers a simple and secure solution for implementing OTP-based authentication in various applications. With its high performance, ease of use, and extensive documentation, FastAPI allows us to build robust and scalable APIs efficiently.

Feel free to explore our API using the provided Swagger documentation and integrate it into your application to enhance security and user authentication.

---

Note: Replace "your-api-base-url" in the Swagger Documentation URL with the actual base URL where your API is deployed.
