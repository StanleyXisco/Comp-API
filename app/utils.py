from pwdlib import PasswordHash
'''This file contains utility implementations that can be used across the application. For example, hashing passwords, verifying passwords, etc.'''


#creating a password hash object using the recommended hashing algorithm
password_hash = PasswordHash.recommended()

# function to hash a password using the password hash object created above
def hash(password: str) :
    return password_hash.hash(password)


# implementation of function to verify a password against a hashed password using the password hash object created above
def verify_password(plain_password: str, hashed_password):
    return password_hash.verify(plain_password, hashed_password)