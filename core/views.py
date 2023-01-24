import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from decouple import config
from .models import Phrase, ArticleTopic, Counter
from .forms import PhraseForm


def home(request):
    # counter, _ = Counter.objects.get_or_create()
    form = PhraseForm()

    return render(request, 'core/home.html', {'form': form})


def ajax_process_request(request):
    try:
        phrase = request.POST.get("topic", None).lower()
        category = request.POST.get("category", None)
        count = request.POST.get("count", None) or 5
        count = int(count) if int(count) < 10 else 5
        out = []
        phrase, _ = Phrase.objects.get_or_create(word=phrase)
        response = send_api_request(phrase, category, count)
        current_count, _ = Counter.objects.get_or_create()
        current_count.count += 1
        current_count.save()
        for title in response:
            if title != "" and title != "\n":
                title = ' '.join(title.rsplit()[1:])
                ArticleTopic.objects.create(phrase=phrase, title=title)
                out.append(title)
        return JsonResponse({"data": out, 'exist': False})
    except Exception as e:
        return JsonResponse({'error': str(e)})


# def ajax_process_request(request):
#     out = []
#     phrase = request.GET.get("topic", None).lower()
#
#     response = send_api_request(phrase)
#     current_count, _ = Counter.objects.get_or_create()
#     current_count.count += 1
#     current_count.save()
#     for title in response:
#         if title != "" and title != "\n":
#             title = ' '.join(title.rsplit()[1:])
#             out.append(title)
#     return JsonResponse({"data": out, 'exist': False, 'counter': current_count.count})


def send_api_request(keyword: str, category: str, count: int):
    api_key = settings.OPEN_API_KEY
    url = "https://api.openai.com/v1/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "text-davinci-003",
        "prompt": f"write out {count} unique, creative and engaging topics for a {category} on {keyword}.",
        "temperature": 0.6,
        "max_tokens": 100,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    d = json.dumps(data)
    response = requests.post(url, headers=headers, data=d)
    output = response.json()
    if not output.get('error'):
        text = output.get('choices')[0].get('text')
        text = text.split('\n')
    else:
        text = ["A server Error due to request overload, Try again..."]
    return text


def check_keyword_exists(keyword: str):
    try:
        phrase = Phrase.objects.get(word=keyword)
        output = [x.title for x in phrase.topics.all()]
        return True, output
    except Phrase.DoesNotExist:
        return False, []

