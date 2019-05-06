#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.models import ExtensionAssets
from woost.models.rendering import ChainRenderer
from .youtubevideorenderer import YouTubeVideoRenderer

def install():
    """Creates the assets required by the youtube extension."""

    assets = ExtensionAssets("youtube")
    content_renderer = ChainRenderer.require_instance(
        qname = "woost.content_renderer"
    )
    youtube_renderer = assets.require(YouTubeVideoRenderer, "renderer")
    content_renderer.renderers.append(youtube_renderer)

