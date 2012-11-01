import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obs_osv_arkiv.settings")
from django.db import models, connection
from archive.models import Item, Category, Materials, Keywords, Condition, Address, Area, Room
#from obs_osv_arkiv import settings


i = Item.objects.get_or_create(item_number="GA_test")

#for line in open('import.csv', 'r'):	
#	i = Item.get_or_create(item_number=field[0])
