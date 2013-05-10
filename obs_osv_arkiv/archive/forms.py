import pdb
from django import forms
from django.forms import widgets
from archive.models import Item, Condition, Tag, Location, Keywords, Materials
from archive.widgets import ManyToManyTextWidget #,KeywordWidget, MaterialWidget, 
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.translation import ugettext_lazy as _


class ItemSearchForm(forms.Form):
    category =  forms.CharField(widget=forms.TextInput(attrs={'id': 'category', 'name': 'category'}), label = _('Category'), required=False)
    title =  forms.CharField(widget=forms.TextInput(attrs={'id': 'title', 'name': 'title'}), label = _('Title'), required=False)
    artist =  forms.CharField(widget=forms.TextInput(attrs={'id': 'artist', 'name': 'artist'}), label = _('Artist'), required=False)
    date_from =  forms.CharField(widget=forms.TextInput(attrs={'id': 'from', 'name': 'from'}), label = _('Dating, From'), required=False)
    date_to =  forms.CharField(widget=forms.TextInput(attrs={'id': 'to', 'name': 'to'}), label = _('Dating, To'), required=False)
    city =  forms.CharField(widget=forms.TextInput(attrs={'id': 'city', 'name': 'city'}), label = _('City'), required=False)
    country =  forms.CharField(widget=forms.TextInput(attrs={'id': 'country', 'name': 'country'}), label = _('Country'), required=False)
    material = forms.CharField(widget=forms.TextInput(attrs={'id': 'material', 'name': 'material'}), label = _('Material'), required=False)
    fulltext = forms.CharField(widget=forms.TextInput(attrs={'id': 'fulltext', 'name': 'fulltext'}), label = _('Fulltext'), required=False)
    checkmovie = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'checkmovie', 'name': 'checkmovie'}), label = _('Item with movies'), required=False)

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


