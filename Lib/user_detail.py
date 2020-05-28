from django.http import HttpResponse
from django.contrib.auth import get_user_model
from jwt import DecodeError

from Lib import redis_cache
from Lib.pyjwt_token import TokenGeneration

User = get_user_model()


def get_user(request, *args, **kwargs):
    try:
        # import pdb
        # pdb.set_trace()
        token = redis_cache.Get('Token')
        if token:
            payload = TokenGeneration.decode_token(token)
            user_id = payload['id']
            user = User.objects.get(id=user_id)
            if user:
                return user
            else:
                return False
        else:
            return False
    except Exception as e:
        return str(e)
