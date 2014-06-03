# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'play_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('score', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=4, decimal_places=0)),
            ('experience', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=5, decimal_places=0)),
            ('level', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=4, decimal_places=0)),
            ('picture_url', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
        ))
        db.send_create_signal(u'play', ['Player'])

        # Adding model 'Shop'
        db.create_table(u'play_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='Super shop!', max_length=100, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'play', ['Shop'])

        # Adding model 'Organization'
        db.create_table(u'play_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='Super Duper!', max_length=100, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'play', ['Organization'])

        # Adding model 'Coupon'
        db.create_table(u'play_coupon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=0)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Shop'])),
        ))
        db.send_create_signal(u'play', ['Coupon'])

        # Adding M2M table for field buyers on 'Coupon'
        m2m_table_name = db.shorten_name(u'play_coupon_buyers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm[u'play.coupon'], null=False)),
            ('player', models.ForeignKey(orm[u'play.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coupon_id', 'player_id'])

        # Adding model 'Event'
        db.create_table(u'play_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('experience', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=5, decimal_places=0)),
            ('points', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=0)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Organization'])),
        ))
        db.send_create_signal(u'play', ['Event'])

        # Adding M2M table for field participants on 'Event'
        m2m_table_name = db.shorten_name(u'play_event_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'play.event'], null=False)),
            ('player', models.ForeignKey(orm[u'play.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'player_id'])

        # Adding model 'Challenge'
        db.create_table(u'play_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('challenge_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('points', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=0)),
        ))
        db.send_create_signal(u'play', ['Challenge'])

        # Adding M2M table for field participants on 'Challenge'
        m2m_table_name = db.shorten_name(u'play_challenge_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm[u'play.challenge'], null=False)),
            ('player', models.ForeignKey(orm[u'play.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['challenge_id', 'player_id'])

        # Adding model 'CouponHistory'
        db.create_table(u'play_couponhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('shop', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Player'])),
        ))
        db.send_create_signal(u'play', ['CouponHistory'])

        # Adding model 'EventHistory'
        db.create_table(u'play_eventhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Player'])),
            ('points', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=0)),
        ))
        db.send_create_signal(u'play', ['EventHistory'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'play_player')

        # Deleting model 'Shop'
        db.delete_table(u'play_shop')

        # Deleting model 'Organization'
        db.delete_table(u'play_organization')

        # Deleting model 'Coupon'
        db.delete_table(u'play_coupon')

        # Removing M2M table for field buyers on 'Coupon'
        db.delete_table(db.shorten_name(u'play_coupon_buyers'))

        # Deleting model 'Event'
        db.delete_table(u'play_event')

        # Removing M2M table for field participants on 'Event'
        db.delete_table(db.shorten_name(u'play_event_participants'))

        # Deleting model 'Challenge'
        db.delete_table(u'play_challenge')

        # Removing M2M table for field participants on 'Challenge'
        db.delete_table(db.shorten_name(u'play_challenge_participants'))

        # Deleting model 'CouponHistory'
        db.delete_table(u'play_couponhistory')

        # Deleting model 'EventHistory'
        db.delete_table(u'play_eventhistory')


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'play.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'challenge_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['play.Player']", 'symmetrical': 'False'}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        u'play.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'buyers': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['play.Player']", 'null': 'True', 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Shop']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        u'play.couponhistory': {
            'Meta': {'object_name': 'CouponHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"}),
            'shop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'play.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'experience': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Organization']"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['play.Player']", 'null': 'True', 'symmetrical': 'False'}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'play.eventhistory': {
            'Meta': {'object_name': 'EventHistory'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'play.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Super Duper!'", 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'play.player': {
            'Meta': {'object_name': 'Player'},
            'experience': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '0'}),
            'picture_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'play.shop': {
            'Meta': {'object_name': 'Shop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Super shop!'", 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['play']