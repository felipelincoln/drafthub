class BaseError:
    def __init__(self):
        self.status = None
        self.verbose = None
        self.message = None
        
    @property
    def context(self):
        context = {
            'status': self.status,
            'verbose': self.verbose,
            'message': self.message,
        }

        return context


class PageContext:
    request = None
    url = 'https://drafthub.herokuapp.com' #change before merge

    def __init__(self, request):
        self.request = request

        self.author = 'Felipe Lincoln'
        self.keywords = None
        self.title = 'drafthub: blog like a developer'
        self.description = 'Start your own developer blog using git and'\
            ' markdown and integrate the GitHub community'
        self.url += request.get_full_path()
        self.image = 'https://i.ibb.co/McvBBRT/drafthub-1.png'
        self.error = BaseError()
        
    @property
    def context(self):
        context = {
            'page_author': self.author,
            'page_keywords': self.keywords,
            'page_title': self.title,
            'page_description': self.description,
            'page_url': self.url,
            'page_image': self.image,
            'page_error': self.error.context,
        }

        return context
