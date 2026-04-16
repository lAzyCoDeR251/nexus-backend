from django.conf import settings

def get_view_count(prompt_id):
    key = f"prompt:{prompt_id}:views"
    count = settings.REDIS_CLIENT.get(key)
    return int(count) if count else 0


def increment_view_count(prompt_id):
    key = f"prompt:{prompt_id}:views"
    return settings.REDIS_CLIENT.incr(key)
