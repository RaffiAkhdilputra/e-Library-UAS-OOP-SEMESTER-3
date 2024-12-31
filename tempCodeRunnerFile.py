import bcrypt
import datetime

# Declaring our password
password = b"Raffi123"

# Adding the salt to password
salt = bcrypt.gensalt()
# Hashing the password
hashed = bcrypt.hashpw(password, salt)

# printing the salt
print("Salt :")
print(salt)

# printing the hashed
print("Hashed")
print(hashed)

# checking the password
check = bcrypt.checkpw(password, hashed)
print(check)

print(str(datetime.date.today().strftime('%Y-%m-%d')))