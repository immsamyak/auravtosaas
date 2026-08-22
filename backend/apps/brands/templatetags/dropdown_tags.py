from django import template

register = template.Library()

@register.tag(name="dropdown")
def do_dropdown(parser, token):
    nodelist = parser.parse(('enddropdown',))
    parser.delete_first_token()
    
    # Optional arguments parsing could go here, but we will keep it simple
    return DropdownNode(nodelist)

class DropdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        # Render the inner content (the forms/links)
        content = self.nodelist.render(context)
        
        # Load the dropdown wrapper template
        t = context.template.engine.get_template('components/dropdown.html')
        
        # Push the inner HTML content to the context and render
        with context.push(dropdown_content=content):
            return t.render(context)
