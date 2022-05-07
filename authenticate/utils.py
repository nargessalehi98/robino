import uuid
from datetime import date

import jwt
from bson import ObjectId
from passlib.context import CryptContext
from authenticate.db import jwt_secret, auth_collection
from authenticate.db import database
from common.utils import get_db_handle, get_collection_handle

pwd_context = CryptContext(
    default="django_pbkdf2_sha256",
    schemes=["django_argon2", "django_bcrypt", "django_bcrypt_sha256",
             "django_pbkdf2_sha256", "django_pbkdf2_sha1",
             "django_disabled"])


def create_unique_object_id():
    unique_object_id = "ID_{uuid}".format(uuid=uuid.uuid4())
    return unique_object_id


# Check if user if already logged in
def login_status(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    data = jwt.decode(token, jwt_secret, algorithms=['HS256'])

    device = str(request.user_agent.device)
    os = str(request.user_agent.os)
    browser = str(request.user_agent.browser)

    user_obj = None
    flag = False
    user_filter = database[auth_collection].find({"password": data["password"]},
                                                 {"email": 0, "password": 0})
    token_status = database['activetokens'].find({"token": token})
    if user_filter.count() and token_status.count():
        flag = True
        user_obj = list(user_filter)[0]
    return flag, user_obj, token, device, browser, os


def check_active_devices(request, user, token):
    old_token = list(database['userprofile'].find({"_id": user["_id"]}))[0]['device']['token']
    remove_active_token(old_token)
    device = {
        "token": token,
        "device": str(request.user_agent.device),
        "os": str(request.user_agent.os),
        "browser": str(request.user_agent.browser)
    }
    database['userprofile'].update_one({"_id": user["_id"]}, {"$set": {"device": device}})
    return True


def remove_active_token(token):
    result = database['activetokens'].remove({"token": token})
    return result


def remove_active_device(user_id, token):
    result = database['userprofile'].find_one_and_update({"_id": user_id},
                                                         {"$pull": {"devices": {"token": token}}})
    if result:
        return True
    return False
