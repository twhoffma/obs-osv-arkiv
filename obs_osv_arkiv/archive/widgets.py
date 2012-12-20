from django.forms import widgets
from archive.models import Tag

from django.forms.util import flatatt
from django.utils.safestring import mark_safe
import pdb

class MaterialWidget(widgets.Widget):
	def render(self, name, value, attrs=None):
		from archive.models import Materials
		#final_attrs = self.build_attrs(attrs, type='text', name=name)
		final_attrs = self.build_attrs(attrs, name=name)
		objects = []
		val = ''
		
		if value:	
			for each in value:
				try:
					tag = Materials.objects.get(pk=each)
					objects.append(tag)
				except:
					continue
			
			values = []
			for each in objects:
				values.append(str(each))
			value = ','.join(values)
			
			if value:
				val = value
				#final_attrs['value'] = value
		else:
			final_attrs['value'] = ''
		return mark_safe(u'<textarea %s >%s</textarea>' % (flatatt(final_attrs), val.decode('utf-8')))

class KeywordWidget(widgets.Widget):
	def render(self, name, value, attrs=None):
		from archive.models import Keywords
		final_attrs = self.build_attrs(attrs, name=name)
		objects = []
		val = ''
		if value:	
			for each in value:
				try:
					tag = Keywords.objects.get(pk=each)
					objects.append(tag)
				except:
					continue
			
			values = []
			
			for each in objects:
				values.append(str(each))
			value = ','.join(values)
			
			if value:
				val = value
				#final_attrs['value'] = value
		else:
			final_attrs['value'] = ''
		return mark_safe(u'<textarea %s >%s</textarea>' % (flatatt(final_attrs), val.decode('utf-8')))

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
					#values.append(u'<span style="background-color: #f6f6f6;">' + str(each) + '</span>')
				value = ','.join(values)
				
				if value:
					val = value
			else:
				final_attrs['value'] = ''
			return mark_safe(u'<textarea %s >%s</textarea>' % (flatatt(final_attrs), val.decode('utf-8')))
		else:
			raise Exception('Widget need to define the cls in attributes!')
