from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=50)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	
	class Meta:
		unique_together = (('name', 'parent'),)
	
	def __unicode__(self):
		category_ancestors = [c.name for c in self.get_ancestors()]
		category_path = category_ancestors.append(self.name)
		return('>'.join(category_path))


