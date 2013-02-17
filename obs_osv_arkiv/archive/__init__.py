from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

from django.db.models.signals import pre_save
from django.dispatch import receiver
from archive.models import Item

from django.db.models.signals import post_save, pre_save

import pdb

#@receiver(pre_save, sender=Item)
def log_loan_status(sender, **kwargs):
	loan_status_changed = False
	
	if kwargs.get('instance').pk:
		item_pk = kwargs['instance'].pk
		item = Item.objects.get(pk=item_pk)
		old_loan_status = item.loan_status
		loan_status = kwargs['instance'].loan_status
		if old_loan_status.lower().strip() != loan_status.lower().strip():
			loan_status_changed = True
	else:
		loan_status_changed = (kwargs['instance'].loan_status.strip() != '')
	pdb.set_trace()
	
	#LogEntry.objects.log_action(
    	#	user_id         = request.user.pk, 
    	#	content_type_id = ContentType.objects.get_for_model(object).pk,
    	#	object_id       = object.pk,
    	#	object_repr     = force_unicode(object), 
    	#	action_flag     = CHANGE
	#)
