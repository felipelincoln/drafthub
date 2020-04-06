from django.core.exceptions import ValidationError
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_github_url(self):
        import re
        import requests

        regex_expr = '^https:\/\/github\.com\/(.+?)\/(.+?)\/blob\/(.*\.md)$'
        regex_tester = re.compile(regex_expr)
        regex_results = regex_tester.match(self.cleaned_data['github_url'])
    
        if not regex_results:
            raise ValidationError('url must be a github .md file.')

        handle, repo, md = regex_results.groups()
        if handle != self.request.user.username:
            raise ValidationError('url must be from your repositories.')

        raw_github_url = f'https://raw.githubusercontent.com/{handle}/{repo}/{md}'
        head_response = requests.head(raw_github_url)
        if head_response.status_code != 200:
            raise ValidationError('not found in your repositories.')

        return self.cleaned_data['github_url']


    class Meta:
        model = Post
        fields = ['title', 'github_url']
