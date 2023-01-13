import json

import requests
from django.http import JsonResponse
from django.shortcuts import render
from decouple import config
from .models import Phrase, ArticleTopic


def home(request):
    return render(request, 'core/home.html')


def ajax_process_request(request):
    phrase = request.GET.get("topic", None)
    exist, out = check_keyword_exists(phrase)
    if not exist:
        out = []
        phrase = Phrase.objects.create(word=phrase)
        response = send_api_request(phrase)
        for title in response:
            if title != "" and title != "\n":
                ArticleTopic.objects.create(phrase=phrase, title=title)
                out.append(title)
    return JsonResponse({"data": out})


def send_api_request(keyword):
    api_key = config("OPEN_API_KEY")
    url = "https://api.openai.com/v1/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "text-davinci-001",
        "prompt": f"List couple technical article topics on {keyword}.",
        # "prompt": "write several Muslim pickup lines for Aeeshah ",
        "temperature": 0.4,
        "max_tokens": 100,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    d = json.dumps(data)
    response = requests.post(url, headers=headers, data=d)
    output = response.json()
    text = output.get('choices')[0].get('text')
    text = text.split('\n')
    return text


def check_keyword_exists(keyword: str):
    try:
        phrase = Phrase.objects.get(word=keyword)
        output = [x.title for x in phrase.topics.all()]
        return True, output
    except Phrase.DoesNotExist:
        return False, []


