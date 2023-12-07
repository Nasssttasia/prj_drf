import re

from rest_framework.exceptions import ValidationError


class YouTubeLink:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link_dict = dict(value).get(self.field)

        link_pattern = r'https?://\S+|www\.\S+'
        youtube_url_pattern = r'(?:https?://)?(?:www\.)?youtube\.com'

        links = re.findall(link_pattern, link_dict)
        for link in links:
            if not bool(re.match(youtube_url_pattern,link)):
                raise ValidationError(f'Только ссылки на YouTube!')
