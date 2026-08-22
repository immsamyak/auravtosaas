from django import template
from django.utils.safestring import mark_safe

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
