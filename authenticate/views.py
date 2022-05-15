from django_user_agents.utils import get_user_agent
from rest_framework.decorators import api_view
from authenticate.utils import create_unique_object_id, pwd_context
from authenticate.db import database, auth_collection, fields, jwt_life, jwt_secret, secondary_username_field
import jwt
import datetime
from authenticate import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .permissions import login_status
from common.utils import password_is_valid
from .utils import check_active_devices, remove_active_token, remove_active_device
from .celery_tasks import CeleryTasksAuth
from brake.decorators import ratelimit


# @ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True)
@ratelimit(field='username', method='POST', rate='1/m')
@api_view(["POST"])
def signup(request):
    try:
        data = request.data if request.data is not None else {}
        signup_data = {}
        signup_data["new_posts"] = []
        signup_data["public"] = "True"
        signup_data["device"] = {"token": "", "device": "", "os": "", "browser": ""}
        all_fields = set(fields + ("email", "username", "password"))
        if secondary_username_field is not None:
            all_fields.add(secondary_username_field)
        for field in set(fields + ("email", "username", "password")):
            if field in data:
                signup_data[field] = data[field]
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"error_msg": field.title() + " does not exist."})
        # if not password_is_valid(signup_data["password"]):
        #     return Response(status=status.HTTP_400_BAD_REQUEST, data={"error_msg": messages.password_error})
        signup_data["password"] = pwd_context.hash(signup_data["password"])
        if database[auth_collection].find_one({"email": signup_data['email']}) is None:
            if secondary_username_field:
                if database[auth_collection].find_one(
                        {secondary_username_field: signup_data[secondary_username_field]}) is None:
                    database[auth_collection].insert_one(signup_data)
                    res = {k: v for k, v in signup_data.items() if k not in ["_id", "password"]}
                    return Response(status=status.HTTP_200_OK,
                                    data={"data": res})
                else:
                    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                                    data={"data": {"error_msg": messages.user_exists_field(secondary_username_field)}})
            else:
                database[auth_collection].insert_one(signup_data)
                res = {k: v for k, v in signup_data.items() if k not in ["_id", "password"]}
                return Response(status=status.HTTP_200_OK,
                                data={"data": res})
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                            data={"data": {"error_msg": messages.user_exists}})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})


@ratelimit(field='username', method='POST', rate='1/m')
@api_view(["POST"])
def login(request):
    try:
        data = request.data if request.data is not None else {}
        username = data['username']
        password = data['password']
        if "@" in username:
            user = database[auth_collection].find_one({"email": username}, {"_id": 0})
        else:
            if secondary_username_field:
                user = database[auth_collection].find_one({secondary_username_field: username})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"data": {"error_msg": messages.user_not_found}})
        if user is not None:
            if pwd_context.verify(password, user["password"]):
                token = jwt.encode({'password': user['password'],
                                    'exp': datetime.datetime.now() + datetime.timedelta(days=jwt_life)},
                                   jwt_secret, algorithm='HS256').decode('utf-8')
                database['activetokens'].insert_one({"token": token})
                check_active_devices(request, user, token)
                return Response(status=status.HTTP_200_OK,
                                data={"data": {"token": token}})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"error_msg": messages.incorrect_password})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"data": {"error_msg": messages.user_not_found}})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})


@ratelimit(field='username', method='POST', rate='1/m')
@api_view(["POST"])
def logout(request):
    try:
        flag, user_obj, token, device, browser, os = login_status(request)
        token = request.META.get('HTTP_AUTHORIZATION')
        if flag:
            remove_active_token(token)
            return Response(status=status.HTTP_200_OK, data={"data": {"message": "logged out"}})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})
