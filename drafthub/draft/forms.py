from django.core.exceptions import ValidationError
from django import forms
from .models import Draft


class DraftForm(forms.ModelForm):
    tags = forms.CharField(max_length=200)


    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_title(self):
        from django.utils.text import slugify
        slug = slugify(self.cleaned_data['title'])

        if slug == '-':
            slug = ''

        if not slug:
            raise ValidationError('invalid title')
        
        return self.cleaned_data['title']
        

    def clean_github_url(self):
        import requests
        from .utils import get_data_from_url

        data = get_data_from_url(self.cleaned_data['github_url'])

        if not data:
            raise ValidationError('url must be a github .md file.')

        login = data['login']
        if login != self.request.user.username:
            raise ValidationError('url must be from your repositories.')

        raw = data['raw']
        head_response = requests.head(raw)
        if head_response.status_code != 200:
            raise ValidationError('not found in your repositories.')

        return self.cleaned_data['github_url']

    def clean_tags(self):
        import re

        TAG_STR = self.cleaned_data['tags']

        def match(pattern):
            re_match = re.compile(pattern)
            return re_match.match(TAG_STR)

        re_comma = '^(?:[\w\s-]+,){0,}(?:[\w\s-]+)?,?$'
        re_size = '^(?:[\w\s-]+,){0,4}(?:[\w\s-]+)?,?$'
        re_length = '^(?:[\w\s-]{1,25},){0,4}(?:[\w\s-]{1,25})?,?$'

        check_comma = match(re_comma)
        check_length = match(re_length)
        check_size = match(re_size)
        
        if not check_comma:
            raise ValidationError('Tags must be separated by a comma (,)')

        if not check_size:
            raise ValidationError('You can only use 5 tags')
        
        if not check_length:
            raise ValidationError('Each tag must have less than 26 characters')

        return self.cleaned_data['tags'].lower()



    class Meta:
        model = Draft
        fields = ['title', 'github_url', 'abstract']
