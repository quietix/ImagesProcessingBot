import json
from django import http
from . import tgbot_services as tgbot
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            request_body = json.loads(request.body)
            my_class = tgbot.Commands_service_class()
            my_class.commands_service_def(request_body)
        except Exception as e:
            print(str(e))

        return http.HttpResponse('', status=200)
    else:
        return http.Http404
