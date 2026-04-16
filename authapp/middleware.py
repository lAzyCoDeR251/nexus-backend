import json
from django.http import JsonResponse
from .jwt import decode_token

class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # protect only POST /prompts
        if request.path.startswith("/prompts") and request.method == "POST":

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return JsonResponse({"error": "No token"}, status=401)

            try:
                token = auth_header.split(" ")[1]
                payload = decode_token(token)

                if not payload:
                    return JsonResponse({"error": "Invalid token"}, status=401)

                # attach user to request (IMPORTANT)
                request.user_payload = payload

            except Exception:
                return JsonResponse({"error": "Unauthorized"}, status=401)

        return self.get_response(request)
