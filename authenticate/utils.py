import uuid
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


def check_active_devices(id, token, device, browser, os):
    db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')
    user_profile_handler = get_collection_handle(db_handler, "userprofile")
    user_profile_handler.find_one_and_update({"_id": ObjectId(id), "devices": {"$size": 3}}, {"$pop": {"devices": -1}})
    device = {
        "token": token,
        "device": device,
        "os": os,
        "browser": browser
    }
    user_profile_handler.find_one_and_update({"_id": ObjectId(id)}, {"$addToSet": {"devices": device}})
