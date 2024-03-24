"""
A script to generate a hashed password for the user

Usage:

    python generate_password.py

"""

from werkzeug.security import generate_password_hash

print("please provide a password: ", end="")
password = input()

hashed_password = generate_password_hash(password)

print(f"Hashed password: {hashed_password}")
