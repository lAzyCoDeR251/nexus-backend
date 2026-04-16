from django.urls import path
from . import views

urlpatterns = [
    path('prompts/', views.list_prompts),          # GET
    path('prompts/create/', views.create_prompt),  # POST
    path('prompts/<int:id>/', views.get_prompt),
]

