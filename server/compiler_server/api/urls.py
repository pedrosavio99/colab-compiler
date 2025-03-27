from django.urls import path
from .views import hello_world, compile_code

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('compile/', compile_code, name='compile_code'),
]