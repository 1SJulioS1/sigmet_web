# from django.http import HttpResponseRedirect
#
#
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            for i in allowed_roles:
                if i in request.user.rol:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrap

    return decorator

