import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obs_osv_arkiv.settings")
from django.db import models, connection
from archive.models import Item, Category, Materials, Keywords, Condition, Address, Area, Room, Location


#i = Item.objects.get_or_create(item_number="GA_test")

n = 0
for line in open('data.csv', 'r'):
	fields = line.split("\t")
	
	n = n + 1 
	
	if n >= 1 and len(fields) == 30:
		item_number = fields[0]
		title = fields[1]
		cat_root1 = fields[2]
		cat_child1 = fields[3]
		cat_root2 = fields[4]
		cat_child2 = fields[5]
		state = fields[6]
		date_certainty = fields[7]
		date_from = fields[8]
		date_to = fields[9]
		prod_certainty = fields[10]
		prod_city = fields[11]
		prod_country = fields[12]
		prod_continent = fields[13]
		artist = fields[14]
		width = fields[15]
		height = fields[16]
		depth = fields[17]
		weight = fields[18]
		material = fields[19]
		prod_place = fields[20]
		#address = fields[21]
		area = fields[21]
		room = fields[22]
		location = fields[23]
		position = fields[24]
		position_alt = fields[25]
		on_loan  = fields[26]
		description = fields[27]
		keywords = fields[28]
		reference_literature = fields[29]
		
		#Get or create item	
		(item, created) = Item.objects.get_or_create(item_number=item_number)
		
		item.title = title
		
		#Categories
		item.category.clear()
		if cat_root1.strip() != "":
			(r, created) = Category.objects.get_or_create(name=cat_root1.strip(), parent=None)
			if cat_child1.strip() != "":
				(c, created) = Category.objects.get_or_create(name=cat_child1.strip(), parent=r)
				item.category.add(c)
			else:
				item.category.add(r)
		
		if cat_root2.strip() != "":
			(r, created) = Category.objects.get_or_create(name=cat_root2.strip(), parent=None)
			if cat_child2.strip() != "":
				(c, created) = Category.objects.get_or_create(name=cat_child2.strip(), parent=r)
				item.category.add(c)
			else:
				item.category.add(r)
		
		if state != "":	
			s = Condition.objects.get(condition_value=state)
			item.condition = s
		
		if date_certainty != "":
			if date_certainty.lower() == "sikker":
				item.dating_certainty = 'Certain'
			else:
				item.dating_certainty = 'Uncertain'
		
		if date_from != "" and int(date_from.strip()):
			item.date_from = int(date_from.strip())
			
		if date_to != "" and int(date_to.strip()):
			item.date_to = int(date_to.strip())
		
		if prod_certainty != "" and prod_certainty != '?':
			if prod_certainty.lower() == "sikker":
				item.origin_certainty = 'Certain'
			else:
				item.origin_certainty = 'Uncertain'
		
		if prod_city != "":
			item.origin_city = prod_city
		
		if prod_country != "":
			item.origin_country = prod_country
		
		if prod_continent != "":
			item.origin_continent = prod_continent
		
		if artist != "":
			item.artist = artist
		
		if height != "" and type(height) == float:
			item.dim_height = height

		if weight != "" and type(weight) == float:
			item.dim_weight = weight
		 
		if width != "" and type(width) == float:
			item.dim_width = width
		
		if depth != "" and type(depth) == float:
			item.dim_depth = depth
		
		if material != "":
			(m, created) = Materials.objects.get_or_create(name=material)
			item.materials.add(m)
				
		#Unused
		#prod_place = fields[20]
		
		(address, created) = Address.objects.get_or_create(name="Blaker")
		item.address = address
		
		if area != "":
			(area, created) = Area.objects.get_or_create(name = area, address = address)
			item.area = area
			
			if room != "":
				(room, created) = Room.objects.get_or_create(name = room, area = area)
				item.room = room
				
				if location != "":
					(loc, created) = Location.objects.get_or_create(name = location, room = room)
					item.location = loc
					
		if position != "":
			item.position = position
		
		#position_alt = fields[25]
		#if position_alt != "":
		#	item.position_alt = position_alt
		
		if on_loan != "":
			item.loan_status = on_loan
		
		if description != "":
			item.description = description
		
		if keywords != "":
			kws = keywords.split(",")
			
			for kw in kws:
				(k, created) = Keywords.objects.get_or_create(name=kw)
				item.keywords.add(k)
		
		if reference_literature != "":
			item.ref_literature = reference_literature	
		
		item.save()
		print(str(n) + " " + cat_root1 + "/" + cat_child1 + " " + cat_root2 + "/" + cat_child2)
	#import pdb
	#pdb.set_trace()
