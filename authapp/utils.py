from django.http import JsonResponse
from .jwt import decode_token

def get_user_from_request(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    parts = auth_header.split(" ")

    if len(parts) != 2:
        return None

    token = parts[1]
    return decode_token(token)

