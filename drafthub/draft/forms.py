from django.core.exceptions import ValidationError
from django import forms
from .models import Draft


class DraftForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False)


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
        from django.utils.text import slugify

        tag_str = self.cleaned_data['tags']
        if not tag_str:
            return None

        def match(pattern):
            re_match = re.compile(pattern)
            return re_match.match(tag_str)

        re_comma = '^(?:[\w\s-]+,){0,}(?:[\w\s-]+)?,?$'
        re_size = '^(?:[\w\s-]+,){0,4}(?:[\w\s-]+)?,?$'
        re_length = '^(?:[\w\s-]{1,25},){0,4}(?:[\w\s-]{1,25})?,?$'
        invalid_re_space = '.*,\s,.*'

        check_comma = match(re_comma)
        check_length = match(re_length)
        check_size = match(re_size)
        check_invalid_space = match(invalid_re_space)

        if not check_comma:
            raise ValidationError('tags must be separated by a comma (,)')

        if not check_size:
            raise ValidationError('you can only use 5 tags')
        
        if not check_length:
            raise ValidationError('each tag must have less than 26 characters')

        if check_invalid_space:
            raise ValidationError('tag name not valid')

        return [slugify(tag) for tag in tag_str.split(',')]


    class Meta:
        model = Draft
        fields = ['title', 'github_url', 'description', 'image']
