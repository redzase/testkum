from django.http import HttpResponse, JsonResponse

def response(code, data=[], message='', status=False, meta=None, json=False, header=None):

    if meta==None and code==200:
        meta = {
            "total": 0,
            "per_page": 0,
            "current_page": 0,
            "last_page": 0,
        }

    res = {
        'code': code,
        'success' : status,
        'message': message,
        'data': data,
        'meta': meta,
    }

    resp = JsonResponse(res, status=code)
    if json:
        resp = JsonResponse(res)

    if header:
        for i in header:
            resp[i] = header[i]

    return resp