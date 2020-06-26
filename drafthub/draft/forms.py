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

        tags = [tag for tag in tag_str.split(', ')]
        bad_tags_len = [tag for tag in tags if len(tag) > 25]
        bad_tags_name = [tag for tag in tags if slugify(tag) in ['', '-']]
        bad_size = len(tags) > 5

        errors = []
        if bad_tags_len:
            errors.append(
                'Tags must have less than 26 characters: '
                +', '.join(bad_tags_len)
            )
        if bad_tags_name:
            errors.append(
                'Invalid tag name: '
                +', '.join(bad_tags_name)
            )
        if bad_size:
            errors.append('Maximum of 5 tags allowed')

        if errors:
            raise ValidationError(errors)

        return [slugify(tag) for tag in tags]


    class Meta:
        model = Draft
        fields = ['title', 'github_url', 'description', 'image']
