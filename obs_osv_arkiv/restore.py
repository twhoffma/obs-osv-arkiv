import os
import sys
import codecs
import pdb

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obs_osv_arkiv.settings")
from django.db import models, connection
from archive.models import Item, Category, Materials, Keywords, Condition, Address, Area, Room, Location, Media, File
from django.core import serializers


file = open('backup.xml', 'r')
file_data = file.read()
file.close()

for obj in serializers.deserialize("xml", file_data):
	obj.save()
