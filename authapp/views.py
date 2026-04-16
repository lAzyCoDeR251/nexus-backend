import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .jwt import generate_token
from django.views.decorators.csrf import csrf_exempt


# REGISTER
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)

        return JsonResponse({
    "message": "User created",
    "user_id": user.id
}, status=201)


# LOGIN

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Missing fields"}, status=400)

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        token = generate_token(user)

        return JsonResponse({
    "token": token,
    "user": {
        "id": user.id,
        "username": user.username
    }
})
