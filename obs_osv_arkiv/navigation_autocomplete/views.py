from django import shortcuts
from django.db.models import Q
from django.contrib.auth.models import User, Group
from archive.models import Item

import pdb

def navigation_autocomplete(request, template_name='navigation_autocomplete/autocomplete.html'):
    
    q = request.GET.get('q', '')
    context = {'q': q}
    
    queries = {}
    queries['users'] = User.objects.filter(
        Q(username__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(email__icontains=q)
    ).distinct()[:3]
    queries['items'] = Item.objects.filter(item_number__icontains=q)#[:3]
    context.update(queries)
    return shortcuts.render(request, template_name, context)
