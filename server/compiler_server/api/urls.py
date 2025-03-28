# api/urls.py

from django.urls import path
from .views import hello_world, compile_code, compiler_syslog_py

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('compile/', compile_code, name='compile_code'),
    path('compile-syslog-py/', compiler_syslog_py, name='compiler_syslog_py'),
]