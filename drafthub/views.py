from django.shortcuts import render


class BaseError:
    def __init__(self):
        self.status = None
        self.verbose = None
        self.title = None
        self.description = None
        self.message = None
        
    @property
    def context(self):
        context = {
            'status': self.status,
            'verbose': self.verbose,
            'title': self.title,
            'description': self.description,
            'message': self.message,
        }

        return context

def error404_view(request, exception):
    error = BaseError()
    error.status = 404
    error.verbose = 'Page not found!'
    error.title = 'drafthub: page not found'
    error.description = 'The page you requested does not exist'
    error.message = 'Is it a bug?'

    return render(request, 'error.html', error.context, status=404)

def error500_view(request):
    error = BaseError()
    error.status = 500
    error.verbose = 'Internal server error!'
    error.title = 'drafthub: Internal server error'
    error.description = 'Something went wrong on the server'
    error.message = '🐛 You just found a bug!'

    return render(request, 'error.html', error.context, status=500)

def error403csrf_view(request, reason=""):
    error = BaseError()
    error.status = 403
    error.verbose = 'Forbidden request!'
    error.title = 'drafthub: forbidden request'
    error.description = 'The request you made was not allowed'
    error.message = 'Did this happen more than once?'

    return render(request, 'error.html', error.context, status=403)

def error400_view(request, exception):
    error = BaseError()
    error.status = 400
    error.verbose = 'Bad request!'
    error.title = 'drafthub: bad request'
    error.description = 'The server could not respond to your request'
    error.message = 'We could not respond to your request.'

    return render(request, 'error.html', error.context, status=400)
