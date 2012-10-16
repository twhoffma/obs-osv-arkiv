# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.published'
        db.add_column('archive_item', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Item.feature_media'
        db.add_column('archive_item', 'feature_media',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='feature_media_set', null=True, to=orm['archive.Media']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.published'
        db.delete_column('archive_item', 'published')

        # Deleting field 'Item.feature_media'
        db.delete_column('archive_item', 'feature_media_id')


    models = {
        'archive.category': {
            'Meta': {'unique_together': "(('name', 'parent'),)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['archive.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'archive.condition': {
            'Meta': {'object_name': 'Condition'},
            'condition_value': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'archive.item': {
            'Meta': {'object_name': 'Item'},
            'aquization_method': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Category']", 'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Condition']"}),
            'date_from': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_to': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dating_certainty': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'dim_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'dim_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'dim_weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'dim_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'era_from': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'era_to': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'feature_media': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'feature_media_set'", 'null': 'True', 'to': "orm['archive.Media']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '14'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'keywords'", 'blank': 'True', 'to': "orm['archive.Tag']"}),
            'loan_status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'materials'", 'blank': 'True', 'to': "orm['archive.Tag']"}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Media']", 'symmetrical': 'False', 'blank': 'True'}),
            'origin_certainty': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'origin_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_continent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ref_literature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topic': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'items'", 'symmetrical': 'False', 'to': "orm['archive.Topic']"})
        },
        'archive.location': {
            'Meta': {'object_name': 'Location'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_ref': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.media': {
            'Meta': {'object_name': 'Media'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'archive.referenceliterature': {
            'Meta': {'object_name': 'ReferenceLiterature'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.topic': {
            'Meta': {'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['archive']