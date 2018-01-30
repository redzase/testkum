import requests
import json

from django.http import HttpResponse, JsonResponse

def curl(url, headers):
    r = requests.get(
        url,
        headers=headers,
    )

    return json.loads(r.text)

def curlPost(url, headers, data):
    r = requests.post(
        url,
        headers=headers,
        data=data
    )

    return json.loads(r.text)

def curlPostJson(url, headers, data):
    r = requests.post(
        url,
        headers=headers,
        json=data
    )

    return r
