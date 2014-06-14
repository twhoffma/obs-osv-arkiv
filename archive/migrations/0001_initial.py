# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemHistory'
        db.create_table(u'archive_itemhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Item'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'archive', ['ItemHistory'])

        # Adding model 'Category'
        db.create_table(u'archive_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['archive.Category'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'archive', ['Category'])

        # Adding unique constraint on 'Category', fields ['name', 'parent']
        db.create_unique(u'archive_category', ['name', 'parent_id'])

        # Adding model 'File'
        db.create_table(u'archive_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Media'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'archive', ['File'])

        # Adding model 'Media'
        db.create_table(u'archive_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('media_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'archive', ['Media'])

        # Adding model 'ItemMedia'
        db.create_table(u'archive_itemmedia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Item'])),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Media'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'archive', ['ItemMedia'])

        # Adding model 'Tag'
        db.create_table(u'archive_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'archive', ['Tag'])

        # Adding model 'Materials'
        db.create_table(u'archive_materials', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'archive', ['Materials'])

        # Adding model 'Keywords'
        db.create_table(u'archive_keywords', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'archive', ['Keywords'])

        # Adding model 'Condition'
        db.create_table(u'archive_condition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('condition_value', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
        ))
        db.send_create_signal(u'archive', ['Condition'])

        # Adding model 'Address'
        db.create_table(u'archive_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('postal_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('postal_area', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'archive', ['Address'])

        # Adding model 'Area'
        db.create_table(u'archive_area', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Address'])),
        ))
        db.send_create_signal(u'archive', ['Area'])

        # Adding unique constraint on 'Area', fields ['name', 'address']
        db.create_unique(u'archive_area', ['name', 'address_id'])

        # Adding model 'Room'
        db.create_table(u'archive_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Area'])),
        ))
        db.send_create_signal(u'archive', ['Room'])

        # Adding unique constraint on 'Room', fields ['name', 'area']
        db.create_unique(u'archive_room', ['name', 'area_id'])

        # Adding model 'Location'
        db.create_table(u'archive_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Room'])),
        ))
        db.send_create_signal(u'archive', ['Location'])

        # Adding unique constraint on 'Location', fields ['name', 'room']
        db.create_unique(u'archive_location', ['name', 'room_id'])

        # Adding model 'Item'
        db.create_table(u'archive_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=14)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Condition'], null=True, blank=True)),
            ('condition_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dating_certainty', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('era_from', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('date_from', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('era_to', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('date_to', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('origin_certainty', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('origin_city', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('origin_country', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('origin_continent', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('origin_provinience', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dim_height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('dim_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('dim_depth', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('dim_weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('ref_literature', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Address'], null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Area'], null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Room'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Location'], null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('loan_status', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('insurance_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'archive', ['Item'])

        # Adding M2M table for field materials on 'Item'
        m2m_table_name = db.shorten_name(u'archive_item_materials')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'archive.item'], null=False)),
            ('materials', models.ForeignKey(orm[u'archive.materials'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'materials_id'])

        # Adding M2M table for field keywords on 'Item'
        m2m_table_name = db.shorten_name(u'archive_item_keywords')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'archive.item'], null=False)),
            ('keywords', models.ForeignKey(orm[u'archive.keywords'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'keywords_id'])

        # Adding M2M table for field category on 'Item'
        m2m_table_name = db.shorten_name(u'archive_item_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'archive.item'], null=False)),
            ('category', models.ForeignKey(orm[u'archive.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'category_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Location', fields ['name', 'room']
        db.delete_unique(u'archive_location', ['name', 'room_id'])

        # Removing unique constraint on 'Room', fields ['name', 'area']
        db.delete_unique(u'archive_room', ['name', 'area_id'])

        # Removing unique constraint on 'Area', fields ['name', 'address']
        db.delete_unique(u'archive_area', ['name', 'address_id'])

        # Removing unique constraint on 'Category', fields ['name', 'parent']
        db.delete_unique(u'archive_category', ['name', 'parent_id'])

        # Deleting model 'ItemHistory'
        db.delete_table(u'archive_itemhistory')

        # Deleting model 'Category'
        db.delete_table(u'archive_category')

        # Deleting model 'File'
        db.delete_table(u'archive_file')

        # Deleting model 'Media'
        db.delete_table(u'archive_media')

        # Deleting model 'ItemMedia'
        db.delete_table(u'archive_itemmedia')

        # Deleting model 'Tag'
        db.delete_table(u'archive_tag')

        # Deleting model 'Materials'
        db.delete_table(u'archive_materials')

        # Deleting model 'Keywords'
        db.delete_table(u'archive_keywords')

        # Deleting model 'Condition'
        db.delete_table(u'archive_condition')

        # Deleting model 'Address'
        db.delete_table(u'archive_address')

        # Deleting model 'Area'
        db.delete_table(u'archive_area')

        # Deleting model 'Room'
        db.delete_table(u'archive_room')

        # Deleting model 'Location'
        db.delete_table(u'archive_location')

        # Deleting model 'Item'
        db.delete_table(u'archive_item')

        # Removing M2M table for field materials on 'Item'
        db.delete_table(db.shorten_name(u'archive_item_materials'))

        # Removing M2M table for field keywords on 'Item'
        db.delete_table(db.shorten_name(u'archive_item_keywords'))

        # Removing M2M table for field category on 'Item'
        db.delete_table(db.shorten_name(u'archive_item_category'))


    models = {
        u'archive.address': {
            'Meta': {'object_name': 'Address'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'postal_area': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postal_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.area': {
            'Meta': {'unique_together': "(('name', 'address'),)", 'object_name': 'Area'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Address']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.category': {
            'Meta': {'unique_together': "(('name', 'parent'),)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['archive.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'archive.condition': {
            'Meta': {'object_name': 'Condition'},
            'condition_value': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'archive.file': {
            'Meta': {'object_name': 'File'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Media']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'archive.item': {
            'Meta': {'object_name': 'Item'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Address']", 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Area']", 'null': 'True', 'blank': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['archive.Category']", 'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_from': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_to': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dating_certainty': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dim_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'dim_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'dim_weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'dim_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'era_from': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'era_to': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'item_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '14'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['archive.Keywords']", 'symmetrical': 'False', 'blank': 'True'}),
            'loan_status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['archive.Materials']", 'symmetrical': 'False', 'blank': 'True'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['archive.Media']", 'symmetrical': 'False', 'through': u"orm['archive.ItemMedia']", 'blank': 'True'}),
            'origin_certainty': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'origin_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_continent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin_provinience': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ref_literature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Room']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.itemhistory': {
            'Meta': {'object_name': 'ItemHistory'},
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Item']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.itemmedia': {
            'Meta': {'object_name': 'ItemMedia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Item']"}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Media']"}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'archive.keywords': {
            'Meta': {'object_name': 'Keywords'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.location': {
            'Meta': {'unique_together': "(('name', 'room'),)", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Room']"})
        },
        u'archive.materials': {
            'Meta': {'object_name': 'Materials'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.media': {
            'Meta': {'object_name': 'Media'},
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'archive.room': {
            'Meta': {'unique_together': "(('name', 'area'),)", 'object_name': 'Room'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Area']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['archive']