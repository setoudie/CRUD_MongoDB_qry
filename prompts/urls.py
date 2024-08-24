from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_prompt, name='create_prompt'),
    path('delete/<str:prompt_id>', views.delete_prompt, name='delete_prompt'),
]