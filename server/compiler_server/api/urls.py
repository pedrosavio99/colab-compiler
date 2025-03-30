# api/urls.py

from django.urls import path
from .views import compiler_syslog_py

urlpatterns = [
    path('compile-syslog-py/', compiler_syslog_py, name='compiler_syslog_py'),
]