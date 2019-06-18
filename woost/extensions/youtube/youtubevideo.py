#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import re
from cocktail.urls import URL
from cocktail import schema
from woost.models import Publishable, url_importer

_video_id_expr = re.compile(r"/(\d+)")

def extract_video_id(string):

    if string:
        match = _video_id_expr.search(string)
        if match:
            return match.group(1)

    return None


class YouTubeVideo(Publishable):

    instantiable = True
    type_group = "resource"
    uri_pattern = "http://youtube.com/watch?v=%s"
    video_player = "cocktail.html.YouTubePlayer"

    default_resource_type = "video"

    members_order = ["title", "video_id"]

    title = schema.String(
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        spellcheck = True,
        member_group = "content"
    )

    video_id = schema.String(
        required = True,
        listed_by_default = False,
        normalization = lambda value: extract_video_id(value) or value,
        member_group = "content"
    )

    def get_uri(self, **kwargs):
        return URL(self.uri_pattern % (self.video_id,))

    def is_internal_content(self, language = None):
        return False


def import_url_as_youtube_video(url_import):

    video_id = extract_video_id(url_import.url)
    if video_id:
        item = YouTubeVideo()
        url_import.apply_scraped_info(item)
        item.video_id = video_id
        return item

    return None

url_importer.prepend_handler(import_url_as_youtube_video)

