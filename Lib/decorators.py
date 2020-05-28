import json

import jwt
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from jwt import DecodeError
from rest_framework import status

from Lib import redis_cache
from Lib.pyjwt_token import TokenGeneration
from Lib.smd_response import SMD_Response


def login_required(any_function):
    def wrapper_function(request, *args, **kwargs):
        try:
            # import pdb
            # pdb.set_trace()
            token = redis_cache.Get('Token')
            details = TokenGeneration.decode_token(token)
            User = get_user_model()
            user = User.objects.get(id=details['id'])
            if user:
                return any_function(request, *args, **kwargs)
            else:
                smd = SMD_Response(message="Something Went Wrong, Please Login Again")
                return HttpResponse(json.dumps(smd), status=status.HTTP_404_NOT_FOUND)
        except DecodeError:
            smd = SMD_Response(status=False, message="Invalid Token", data=[])
            return HttpResponse(json.dumps(smd), status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            smd = SMD_Response(message="Something went wrong(INVALID TOKEN or Details"
                                       ", Please provide Token and Login Again!!!!!")
            return HttpResponse(json.dumps(smd), status=status.HTTP_400_BAD_REQUEST)

    return wrapper_function
