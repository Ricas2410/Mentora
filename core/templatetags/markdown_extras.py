from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    """
    Convert markdown text to HTML
    """
    if not text:
        return ''
    
    # Configure markdown with extensions for better formatting
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Return as safe HTML
    return mark_safe(html)
