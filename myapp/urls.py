from django.urls import path
from .views import register, login, sloves_list_create, sloves_detail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('sloves/', sloves_list_create, name='sloves-list-create'),
    path('sloves/<int:pk>/', sloves_detail, name='sloves-detail'),
]
