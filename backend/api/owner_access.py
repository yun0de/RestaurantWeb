from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


OWNER_GROUP_NAME = "Owner"


def is_owner_user(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=OWNER_GROUP_NAME).exists()


def owner_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_owner_user(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper
