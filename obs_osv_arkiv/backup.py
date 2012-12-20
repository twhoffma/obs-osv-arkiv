import os
import sys
import codecs
import pdb

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obs_osv_arkiv.settings")
from django.db import models, connection
from archive.models import Item, Category, Materials, Keywords, Condition, Address, Area, Room, Location, Media, File, ItemMedia, Tag
from django.core import serializers


obj = list(Category.objects.all()) + list(Materials.objects.all()) + list(Keywords.objects.all()) + list(Condition.objects.all()) + list(Address.objects.all()) + list(Area.objects.all()) + list(Room.objects.all()) + list(Location.objects.all()) + list(File.objects.all()) + list(Media.objects.all()) + list(Item.objects.all()) + list(ItemMedia.objects.all()) + list(Tag.objects.all())

file = open('backup.xml', 'w')
#data = serializers.serialize("xml", list(Item.objects.all()))
data = serializers.serialize("xml", obj)
file.write(data)
file.close()
