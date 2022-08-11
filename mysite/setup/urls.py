from django.urls import re_path
import sys


sys.path.append(f'C:\\Users\\Admin\\PycharmProjects\\pythonProject')
from mysite.tgbot import views


urlpatterns = [
    re_path('^$', views.telegram_webhook)
]
