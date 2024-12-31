import json
import bcrypt

# Load database
with open('database/account.json', 'r') as file:
    data = json.load(file)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def verify_login(username:str, password:str):
    for user in data:
        if user["email"] == username.lower():
            if not check_password(password, user["hashed"].encode('utf-8')):  # Decode stored hash for comparison
                return False, "Wrong password"
            return True, ""
    return False, "User not found"

def get_user(username:str):
    for user in data:
        if user["email"] == username.lower():
            return user

def get_name(username:str):
    for user in data:
        if user["email"] == username.lower():
            first_name = user["content"]["firstName"]
            last_name = user["content"]["lastName"]
            return first_name, last_name

def get_tempat_tanggal_lahir(username:str):
    for user in data:
        if user["email"] == username.lower():
            tempat = user["content"]["tempat"]
            tanggal_lahir = user["content"]["tanggalLahir"]
            bulan_lahir = user["content"]["bulanLahir"]
            tahun_lahir = user["content"]["tahunLahir"]
            return tempat, tanggal_lahir, bulan_lahir, tahun_lahir

def get_bookshelf(username:str):
    for user in data:
        if user["email"] == username.lower():
            return user["content"]["bookshelf"]

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# BUAT PROFILE
# ISI BOOKSHELF
# BUTTON SIMPAN BUKU MASUK KE BOOKSHELF
# FITUR REGISTER