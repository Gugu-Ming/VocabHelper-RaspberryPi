class IPMiddleware(object):
    def process_request(self, request):
        print('Request from {0}:' .format( str(get_client_ip(request)) ))
        return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip