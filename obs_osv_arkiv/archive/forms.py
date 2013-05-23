import pdb
from django import forms
from django.forms import widgets
from archive.models import Item, Condition, Tag, Location, Keywords, Materials
from archive.widgets import ManyToManyTextWidget #,KeywordWidget, MaterialWidget, 
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.translation import ugettext as _


class ItemSearchForm(forms.Form):
    categories = forms.CharField(label=_('Category'), required=False)
    title = forms.CharField(label=_('Title'), required=False)
    artist = forms.CharField(label=_('Artist'), required=False)
    date_from = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': _('FROM')}), label=_('Dating, from'), required=False)
    date_to = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': _('TO')}), label=_('Dating, to'), required=False)
    origin_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('BY')}), label=_('City'), required=False)
    origin_country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('LAND')}), label=_('Country'), required=False)
    materials = forms.CharField(label=_('Material/technique'), required=False)
    q = forms.CharField(label=_('Fulltext'), required=False)
    video_only = forms.BooleanField(widget=forms.CheckboxInput, label=_('Item with movies'), required=False)

class ItemAdminForm(forms.ModelForm):
    materials = forms.CharField(widget=ManyToManyTextWidget(attrs={'rows': 3, 'cls': Materials}), required=False, label=_("Materials"))
    keywords = forms.CharField(widget=ManyToManyTextWidget(attrs={'rows': 3, 'cls': Keywords}), required=False, label=_("Keywords"))

    class Meta:
        model = Item

    def clean(self):
        self.cleaned_data = super(ItemAdminForm, self).clean()
        #lookup and link materials
        materials = []
        keywords = []


        for material in self.cleaned_data['materials'].split(','):
            if len(material.strip()) > 0:
                if Materials.objects.filter(name=material.strip()).count() > 0:
                    m = Materials.objects.filter(name=material.strip())[0]
                else:
                    m = Materials(name=material.strip())
                    m.save()

                materials.append(m)

        for keyword in self.cleaned_data['keywords'].split(','):
            if len(keyword.strip()) > 0:
                if Keywords.objects.filter(name=keyword.strip()).count() > 0:
                    k = Keywords.objects.filter(name=keyword.strip())[0]
                else:
                    k = Keywords(name=keyword.strip())
                    k.save()

                keywords.append(k)

        self.cleaned_data['materials'] = materials
        self.cleaned_data['keywords'] = keywords

        return(self.cleaned_data)


