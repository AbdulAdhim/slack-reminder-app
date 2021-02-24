from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Reply

VERIFICATION_TOKEN = 'dmUadzru9OWWqLfS1v23mcdC'
CALLBACK_HOW_ARE_YOU = 'how_are_you'

@csrf_exempt
def hello(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']

    result = {
        'text': '<@{}> How are you?'.format(user_id),
        'response_type': 'in_channel',
        'attachments' : [
            {
                'text': 'I am :',
                'callback_id' : CALLBACK_HOW_ARE_YOU,
                'fallback': 'fallback',
                'actions': [
                    {
                        'name': 'response',
                        'type': 'select',
                        'text': 'Select your response...',
                        'options': [
                            {
                                'text' : 'fine.',
                                'value' : 'positive'
                            },
                            {
                                'text' : 'so so.',
                                'value' : 'neutral'
                            }, 
                            {
                                'text' : 'terrible.',
                                'value' : 'negative'
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return JsonResponse(result)

@csrf_exempt
def reply(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    payload = json.loads(request.POST.get('payload'))
    if payload.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    if payload.get('callback_id') != CALLBACK_HOW_ARE_YOU:
        raise SuspiciousOperation('Invalid request.')
    
    user = payload['user']
    selected_value = payload['actions'][0]['selected_options'][0]['value']

    if selected_value == 'positive':
        reply = Reply(user_name=user['name'], user_id=user['id'], response=Reply.POSITIVE)
        reply.save()
        result = {
            'text': '<@{}> Great! :smile:'.format(user['id'])
        }
    elif selected_value == 'neutral':
        reply = Reply(user_name=user['name'], user_id=user['id'], response=Reply.NEUTRAL)
        reply.save()
        result = {
            'text': '<@{}> Ok, thank you! :sweat_smile:'.format(user['id'])
        }
    else:
        reply = Reply(user_name=user['name'], user_id=user['id'], response=Reply.NEGATIVE)
        reply.save()
        result = {
            'text': '<@{}> Good luck! :innocent:'.format(user['id'])
        }

    return JsonResponse(result)

def index(request):
    positive_replies = Reply.objects.filter(response=Reply.POSITIVE)
    neutral_replies = Reply.objects.filter(response=Reply.NEUTRAL)
    negative_replies = Reply.objects.filter(response=Reply.NEGATIVE)

    context = {
        'positive_replies': positive_replies,
        'neutral_replies': neutral_replies,
        'negative_replies': negative_replies,

    }
    return render(request, 'index.html', context)

def clear(request):
    Reply.objects.all().delete()
    return HttpResponseRedirect(reverse(index))