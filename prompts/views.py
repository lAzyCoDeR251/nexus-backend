import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Prompt
from authapp.utils import get_user_from_request


# GET ALL PROMPTS
def list_prompts(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    prompts = Prompt.objects.all()

    data = [
        {
            "id": p.id,
            "title": p.title,
            "complexity": p.complexity,
            "created_at": p.created_at.isoformat(),
            "view_count": p.view_count
        }
        for p in prompts
    ]

    return JsonResponse(data, safe=False)


# CREATE PROMPT (PROTECTED)
@csrf_exempt
def create_prompt(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = get_user_from_request(request)

    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    data = json.loads(request.body)

    title = data.get("title")
    content = data.get("content")
    complexity = data.get("complexity")

    errors = {}

    if not title or len(title) < 3:
        errors["title"] = "Min 3 chars"

    if not content or len(content) < 20:
        errors["content"] = "Min 20 chars"

    if not isinstance(complexity, int) or complexity < 1 or complexity > 10:
        errors["complexity"] = "1-10 only"

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    prompt = Prompt.objects.create(
        title=title,
        content=content,
        complexity=complexity
    )

    return JsonResponse({
        "id": prompt.id,
        "message": "Created"
    }, status=201)


# GET SINGLE PROMPT
def get_prompt(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        prompt = Prompt.objects.get(id=id)
    except Prompt.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    # increment view count (SQLite)
    prompt.view_count += 1
    prompt.save(update_fields=["view_count"])

    return JsonResponse({
        "id": prompt.id,
        "title": prompt.title,
        "content": prompt.content,
        "complexity": prompt.complexity,
        "created_at": prompt.created_at.isoformat(),
        "view_count": prompt.view_count
    })
