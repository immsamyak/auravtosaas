from django import template
from django.utils.safestring import mark_safe
import re
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def highlight(text, word):
    """
    Highlights a specific word in the text with a professional gradient italic font.
    Usage: {{ cms.hero_headline|highlight:"AI fitting room" }}
    """
    if not text or not word:
        return text
    
    # The stylized HTML we want to inject around the word
    highlighted_html = f"<span class='text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-purple-600 to-rose-500 italic pr-2' style='font-family: \"Playfair Display\", serif; font-weight: 600;'>{word}</span>"
    
    # Replace the word in the text and return as safe HTML
    result = text.replace(word, highlighted_html)
    return mark_safe(result)

@register.filter
def embed_url(value):
    """
    Production-ready video URL parser.
    Converts various YouTube/Vimeo formats into clean, privacy-enhanced embed URLs.
    Handles: watch, youtu.be, embed, shorts, live, Vimeo, and raw <iframe> HTML.
    """
    if not value:
        return value
        
    # Extract src if an iframe was pasted
    if '<iframe' in value.lower():
        src_match = re.search(r'src=["\'](.*?)["\']', value, re.IGNORECASE)
        if src_match:
            value = src_match.group(1)
            
    # Clean up any trailing/leading whitespace or quotes
    value = value.strip('\'" ')

    # YouTube regex to capture the 11-character video ID
    yt_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?|shorts|live)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    yt_match = re.search(yt_regex, value)
    if yt_match:
        video_id = yt_match.group(1)
        # Use youtube-nocookie.com for better privacy and fewer playback/CSP errors.
        # Minimal clean parameters. Removed autoplay to prevent browser blocking issues.
        return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0"
        
    # Vimeo regex to capture the video ID
    vimeo_regex = r'(?:vimeo\.com\/(?:video\/|channels\/(?:\w+\/)?|groups\/(?:[^\/]*)\/videos\/|album\/(?:\d+)\/video\/|)(\d+)(?:$|\/|\?))'
    vimeo_match = re.search(vimeo_regex, value)
    if vimeo_match:
        video_id = vimeo_match.group(1)
        return f"https://player.vimeo.com/video/{video_id}?title=0&byline=0&portrait=0"
        
    return value

class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ""

@register.tag(name="captureas")
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)
