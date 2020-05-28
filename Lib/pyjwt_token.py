import jwt


class TokenGeneration:
    def encode_token(self, user):
        payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256').decode('utf-8')
        return token

    def decode_token(token):
        details = jwt.decode(token, 'SECRET_KEY', algorithm='HS256')
        return details
