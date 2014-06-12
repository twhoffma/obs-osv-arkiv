from django.forms import widgets
from archive.models import Tag

from django.forms.util import flatatt
from django.utils.safestring import mark_safe
import pdb

class ManyToManyTextWidget(widgets.Widget):
	def render(self, name, value, attrs=None):
		cls = self.attrs.get('cls')
		if cls:
			del self.attrs['cls']
			
			final_attrs = self.build_attrs(attrs, name=name)
			objects = []
			val = ''
			if value:	
				for each in value:
					try:
						tag = cls.objects.get(pk=each)
						objects.append(tag)
					except:
						continue
				
				values = []
				
				for each in objects:
					values.append(str(each))
				value = ','.join(values)
				
				if value:
					val = value
			else:
				final_attrs['value'] = ''
			return mark_safe(u'<textarea %s >%s</textarea>' % (flatatt(final_attrs), val.decode('utf-8')))
		else:
			raise Exception('Widget need to define the cls in attributes!')
