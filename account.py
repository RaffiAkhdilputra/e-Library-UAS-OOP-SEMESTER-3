import json
import bcrypt
import datetime

# Load database
with open('database/account.json', 'r') as file:
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
            if not check_password(password, user["hashed"].encode('utf-8')):  # Decode stored hash for comparison
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

    with open('database/account.json', 'w') as file:
        json.dump(data, file, indent=4)

def edit_nama(target, firstName, lastName):
    for user in data:
        if user["email"].lower() == target.lower():
            user["content"]["firstName"] = firstName
            user["content"]["lastName"] = lastName

def edit_tempat_tanggal_lahir(target, tempat, tanggal_lahir, bulan_lahir, tahun_lahir):
    for user in data:
        if user["email"].lower() == target.lower():
            user["content"]["tempat"] = tempat
            user["content"]["tanggalLahir"] = tanggal_lahir
            user["content"]["bulanLahir"] = bulan_lahir
            user["content"]["tahunLahir"] = tahun_lahir

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