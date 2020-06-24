from django.shortcuts import render
from drafthub.utils import PageContext


def error404_view(request, exception):
    page_meta = PageContext(request)
    page_meta.error.status = 404
    page_meta.error.verbose = 'Page not found!'
    page_meta.error.message = 'Is it a bug?'
    page_meta.title = 'drafthub: page not found'
    page_meta.description = 'The page you requested does not exist'

    return render(request, 'error.html', page_meta.context, status=404)

def error500_view(request):
    page_meta = PageContext(request)
    page_meta.error.status = 500
    page_meta.error.verbose = 'Internal server error!'
    page_meta.error.message = '🐛 You just found a bug!'
    page_meta.title = 'drafthub: Internal server error'
    page_meta.description = 'Something went wrong on the server'

    return render(request, 'error.html', page_meta.context, status=500)

def error403csrf_view(request, reason=""):
    page_meta = PageContext(request)
    page_meta.error.status = 403
    page_meta.error.verbose = 'Forbidden request!'
    page_meta.error.message = 'Did this happen more than once?'
    page_meta.title = 'drafthub: forbidden request'
    page_meta.description = 'The request you made was not allowed'

    return render(request, 'error.html', page_meta.context, status=403)

def error400_view(request, exception):
    page_meta = PageContext(request)
    page_meta.error.status = 400
    page_meta.error.verbose = 'Bad request!'
    page_meta.error.message = 'We could not respond to your request.'
    page_meta.title = 'drafthub: bad request'
    page_meta.description = 'The server could not respond to your request'

    return render(request, 'error.html', page_meta.context, status=400)
