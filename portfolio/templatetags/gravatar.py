import hashlib
from urllib.parse import urlencode
from django import template
from django.utils.safestring import mark_safe
 
register = template.Library()
 
@register.filter
def gravatar_url(email, size=30):
    default = "https://example.com/static/images/defaultavatar.jpg"
    email_encoded = email.lower().encode('utf-8')
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    params = urlencode({'d': default, 's': str(size)})
    return f"https://www.gravatar.com/avatar/{email_hash}?{params}"
 
@register.filter
def gravatar(email, size=30):
    url = gravatar_url(email, size)
    return mark_safe(f'')