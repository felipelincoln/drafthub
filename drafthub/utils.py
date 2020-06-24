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


class PageContext:
    def __init__(self):
        self.title = 'drafthub: blog like a developer'
        self.description = 'Start your own developer blog using git and'\
            ' markdown and integrate the GitHub community'
        self.url = 'https://drafthub-development.herokuapp.com' #change before merge
        self.image = 'https://i.ibb.co/McvBBRT/drafthub-1.png'
        
    @property
    def context(self):
        context = {
            'page_title': self.title,
            'page_description': self.description,
            'page_url': self.url,
            'page_image': self.image,
        }

        return context
