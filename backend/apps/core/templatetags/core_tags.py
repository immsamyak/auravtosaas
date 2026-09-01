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
    Converts a standard YouTube or Vimeo URL into its embeddable version.
    If the user pastes an entire <iframe> HTML tag, it extracts the src URL.
    - <iframe src="https://www.youtube.com/embed/VIDEO_ID"... -> https://www.youtube.com/embed/VIDEO_ID
    - https://youtu.be/VIDEO_ID -> https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID -> https://www.youtube.com/embed/VIDEO_ID
    - https://vimeo.com/VIDEO_ID -> https://player.vimeo.com/video/VIDEO_ID
    """
    if not value:
        return value
        
    # If the user pasted an iframe tag, extract the src
    if '<iframe' in value.lower():
        src_match = re.search(r'src=["\'](.*?)["\']', value, re.IGNORECASE)
        if src_match:
            value = src_match.group(1)
            
    try:
        parsed_url = urlparse(value)
        
        # Handle youtu.be
        if 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
            
        # Handle youtube.com
        elif 'youtube.com' in parsed_url.netloc:
            if 'watch' in parsed_url.path:
                qs = parse_qs(parsed_url.query)
                video_id = qs.get('v', [None])[0]
                if video_id:
                    return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
            # Already an embed or other path?
            return value
            
        # Handle vimeo.com
        elif 'vimeo.com' in parsed_url.netloc and 'player.vimeo.com' not in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            return f"https://player.vimeo.com/video/{video_id}?autoplay=1"
            
    except Exception:
        pass
        
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
