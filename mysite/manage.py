#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import telepot


token = '5099222715:AAFChikYgr5R3m0ezz9H0jhHVnKdInvrtGo'


TelegramBot = telepot.Bot(token)
telepot.Bot(token).deleteWebhook()
telepot.Bot(token).setWebhook('https://5074-176-98-31-129.ngrok.io/')

