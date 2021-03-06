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
            ('score', self.gf('django.db.models.fields.DecimalField')(default=20, null=True, max_digits=4, decimal_places=0)),
            ('experience', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=5, decimal_places=0)),
            ('level', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=4, decimal_places=0)),
            ('picture_url', self.gf('django.db.models.fields.CharField')(default='/static/img/avatar-1.png', max_length=200, null=True)),
        ))
        db.send_create_signal(u'play', ['Player'])

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

        # Adding model 'Idea'
        db.create_table(u'play_idea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
            ('points', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=0)),
            ('experience', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=5, decimal_places=0)),
        ))
        db.send_create_signal(u'play', ['Idea'])

        # Adding model 'Comment'
        db.create_table(u'play_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
            ('commenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Player'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['charity.Event'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True)),
        ))
        db.send_create_signal(u'play', ['Comment'])

        # Adding model 'Feed'
        db.create_table(u'play_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Player'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['charity.Event'])),
            ('likes', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True)),
        ))
        db.send_create_signal(u'play', ['Feed'])

        # Adding model 'CommentFeed'
        db.create_table(u'play_commentfeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
            ('commenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Player'])),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Feed'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True)),
        ))
        db.send_create_signal(u'play', ['CommentFeed'])

        # Adding model 'Badge'
        db.create_table(u'play_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['play.Player'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='Beginner!', max_length=100, null=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(default='fa-thumbs-o-up', max_length=50)),
        ))
        db.send_create_signal(u'play', ['Badge'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'play_player')

        # Deleting model 'CouponHistory'
        db.delete_table(u'play_couponhistory')

        # Deleting model 'EventHistory'
        db.delete_table(u'play_eventhistory')

        # Deleting model 'Idea'
        db.delete_table(u'play_idea')

        # Deleting model 'Comment'
        db.delete_table(u'play_comment')

        # Deleting model 'Feed'
        db.delete_table(u'play_feed')

        # Deleting model 'CommentFeed'
        db.delete_table(u'play_commentfeed')

        # Deleting model 'Badge'
        db.delete_table(u'play_badge')


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
        u'charity.event': {
            'Meta': {'object_name': 'Event'},
            'challenge_event': ('django.db.models.fields.CharField', [], {'default': "'Event'", 'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'experience': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['charity.Organization']"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['play.Player']", 'null': 'True', 'symmetrical': 'False'}),
            'picture_url': ('django.db.models.fields.CharField', [], {'default': "'/static/img/stanford.png'", 'max_length': '200', 'null': 'True'}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'charity.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Super Duper!'", 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'play.badge': {
            'Meta': {'object_name': 'Badge'},
            'icon': ('django.db.models.fields.CharField', [], {'default': "'fa-thumbs-o-up'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Beginner!'", 'max_length': '100', 'null': 'True'})
        },
        u'play.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['charity.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'play.commentfeed': {
            'Meta': {'object_name': 'CommentFeed'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'play.couponhistory': {
            'Meta': {'object_name': 'CouponHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"}),
            'shop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
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
        u'play.feed': {
            'Meta': {'object_name': 'Feed'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['charity.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '0'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['play.Player']"})
        },
        u'play.idea': {
            'Meta': {'object_name': 'Idea'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'experience': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'play.player': {
            'Meta': {'object_name': 'Player'},
            'experience': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '0'}),
            'picture_url': ('django.db.models.fields.CharField', [], {'default': "'/static/img/avatar-1.png'", 'max_length': '200', 'null': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '20', 'null': 'True', 'max_digits': '4', 'decimal_places': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['play']