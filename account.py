import os
import sys
import json
import bcrypt
import datetime

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

database_path = resource_path("database/account.json")

if not os.path.exists(database_path):
    raise FileNotFoundError(f"File not found: {database_path}")

# Contoh membuka file
with open(database_path, 'r') as file:
    data = json.load(file)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def verify_login(email:str, password:str):
    for user in data:
        if user["email"] == email.lower():
            if not check_password(password, user["hashed"].encode('utf-8')):
                return False, "Wrong password"
            return True, ""
    return False, "User not found"

def add_new_account(email, confirmed_password, first_name, last_name, tempat, tanggal_lahir, bulan_lahir, tahun_lahir):
    for user in data:
        if user["email"].lower() == email:
            return False, "User already exists"

    hash = hash_password(confirmed_password)

    new_user = {
        "_id": len(data),
        "email": email,
        "hashed": hash.decode('utf-8'),
        "content": {
            "firstName": first_name,
            "lastName": last_name,
            "tempat": tempat,
            "tanggalLahir": tanggal_lahir,
            "bulanLahir": bulan_lahir,
            "tahunLahir": tahun_lahir,
            "tanggalDibuat": datetime.date.today().strftime('%Y-%m-%d'),
            "bookshelf": []
        }
    }

    data.append(new_user)

    with open(database_path, 'w') as file:
        json.dump(data, file, indent=4)

def save_changes():
    with open(database_path, 'w') as file:
        json.dump(data, file, indent=4)

def edit_nama(email, firstName, lastName):
    for user in data:
        if user["email"].lower() == email.lower():
            user["content"]["firstName"] = firstName
            user["content"]["lastName"] = lastName

def edit_tempat_tanggal_lahir(email, tempat, tanggal_lahir, bulan_lahir, tahun_lahir):
    for user in data:
        if user["email"].lower() == email.lower():
            user["content"]["tempat"] = tempat
            user["content"]["tanggalLahir"] = tanggal_lahir
            user["content"]["bulanLahir"] = bulan_lahir
            user["content"]["tahunLahir"] = tahun_lahir

def get_user(email:str):
    for user in data:
        if user["email"].lower() == email.lower():
            return user

def _get_email(email:str):
    for user in data:
        if user["email"] == email.lower():
            return user

def _get_name(email:str):
    for user in data:
        if user["email"] == email.lower():
            first_name = user["content"]["firstName"]
            last_name = user["content"]["lastName"]
            return first_name, last_name

def _get_tempat_tanggal_lahir(email:str):
    for user in data:
        if user["email"] == email.lower():
            tempat = user["content"]["tempat"]
            tanggal_lahir = user["content"]["tanggalLahir"]
            bulan_lahir = user["content"]["bulanLahir"]
            tahun_lahir = user["content"]["tahunLahir"]
            return tempat, tanggal_lahir, bulan_lahir, tahun_lahir

def get_bookshelf(email:str):
    for user in data:
        if user["email"] == email.lower():
            return user["content"]["bookshelf"]
        
def add_book_to_bookshelf(email, book_id):
    for user in data:
        if user["email"] == email.lower():
            for book in user["content"]["bookshelf"]:
                if book == book_id:
                    return
            user["content"]["bookshelf"].append(book_id)

def remove_book_from_bookshelf(email, book_id):
    for user in data:
        if user["email"] == email.lower():
            user["content"]["bookshelf"].remove(book_id)