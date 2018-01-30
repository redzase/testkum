from rest_framework import exceptions, status
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print(["ERRORS:", exc, context, response])
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = response.status_code
        response.data['success'] = False
        # response.data['message'] = 'whoops! we have a problem here'

        if response.status_code == 404:
            response.data['message'] = 'data not found'
        elif response.status_code == 403:
            response.data['message'] = 'permission denied'
        elif response.status_code == 401:
            response.data['message'] = 'unauthorized'
        else:
            response.data['message'] = exc.args[0]
        
        response.data['data'] = []
        response.data['meta'] = None

        response.data.pop('detail')
    else:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'success': False,
            'message': exc.args[0],
            'data': [],
            'meta': None,
        }
        response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response