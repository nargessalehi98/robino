from rest_framework import permissions
from authenticate.utils import login_status
from .utils import check_active_devices


class AuthenticatedOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            flag, user_obj, token, device, browser, os = login_status(request)
            check_active_devices(user_obj["_id"], token , device,browser,os)
            request.user = None
            if flag:
                request.user = user_obj
                return True
            else:
                return False
        except Exception as e:
            return False
