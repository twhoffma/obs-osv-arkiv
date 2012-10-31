# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Area'
        db.create_table('archive_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Address'])),
        ))
        db.send_create_signal('archive', ['Area'])

        # Adding unique constraint on 'Area', fields ['name', 'address']
        db.create_unique('archive_area', ['name', 'address_id'])

        # Adding model 'Room'
        db.create_table('archive_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Area'])),
        ))
        db.send_create_signal('archive', ['Room'])

        # Adding unique constraint on 'Room', fields ['name', 'area']
        db.create_unique('archive_room', ['name', 'area_id'])

        # Adding model 'Address'
        db.create_table('archive_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('postal_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('postal_area', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['Address'])

        # Adding field 'Item.address'
        db.add_column('archive_item', 'address',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Address'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.area'
        db.add_column('archive_item', 'area',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Area'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.room'
        db.add_column('archive_item', 'room',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Room'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.position'
        db.add_column('archive_item', 'position',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Room', fields ['name', 'area']
        db.delete_unique('archive_room', ['name', 'area_id'])

        # Removing unique constraint on 'Area', fields ['name', 'address']
        db.delete_unique('archive_area', ['name', 'address_id'])

        # Deleting model 'Area'
        db.delete_table('archive_area')

        # Deleting model 'Room'
        db.delete_table('archive_room')

        # Deleting model 'Address'
        db.delete_table('archive_address')

        # Deleting field 'Item.address'
        db.delete_column('archive_item', 'address_id')

        # Deleting field 'Item.area'
        db.delete_column('archive_item', 'area_id')

        # Deleting field 'Item.room'
        db.delete_column('archive_item', 'room_id')

        # Deleting field 'Item.position'
        db.delete_column('archive_item', 'position')


    models = {
        'archive.address': {
            'Meta': {'object_name': 'Address'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'postal_area': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postal_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.area': {
            'Meta': {'unique_together': "(('name', 'address'),)", 'object_name': 'Area'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
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
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Address']", 'null': 'True', 'blank': 'True'}),
            'aquization_method': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Area']", 'null': 'True', 'blank': 'True'}),
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
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Keywords']", 'symmetrical': 'False', 'blank': 'True'}),
            'loan_status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Materials']", 'symmetrical': 'False', 'blank': 'True'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Media']", 'symmetrical': 'False', 'blank': 'True'}),
            'origin_certainty': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'origin_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_continent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ref_literature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Room']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.keywords': {
            'Meta': {'object_name': 'Keywords'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.location': {
            'Meta': {'object_name': 'Location'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_ref': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.materials': {
            'Meta': {'object_name': 'Materials'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.media': {
            'Meta': {'object_name': 'Media'},
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'archive.room': {
            'Meta': {'unique_together': "(('name', 'area'),)", 'object_name': 'Room'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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