# coding: utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
from bot.bot import bot
from settings import development


'''@csrf_exempt
def get_message(request):
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse('!', 200)
    return HttpResponse('Method Not Allowed', 405)


bot.set_webhook(url=f'h1km4t1ll0.space/{development.TOKEN}')'''
