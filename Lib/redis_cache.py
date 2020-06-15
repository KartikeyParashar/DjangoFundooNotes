import redis

# When running localhost
# redis_object = redis.Redis(host="localhost", port=6379)

# When running inside Docker use this
redis_object = redis.Redis(host="redis", port=6379)


def Set(username, token):
    """
    :param username: saving token
    :param token:this our actual token
    :return:in this function we save token in redis
    """
    try:
        redis_object.set(username, token)
    except Exception:
        return False


def Get(username):
    """
    :param username: key for get token
    :return:this function used for get token from redis
    """
    try:
        return redis_object.get(username)
    except Exception:
        return False


def Del(username):
    """
    :param username: kye for delete token
    :return: this function used for delete token from redis
    """
    try:

        redis_object.delete(username)

    except Exception:
        return False


def All_Delete():
    """
    :return: this function used for delete all token from redis
    """
    try:
        redis_object.flushall()
    except Exception:
        return False



