# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BlogPost.url'
        db.delete_column(u'blog_blogpost', 'url')

        # Adding field 'BlogPost.slug'
        db.add_column(u'blog_blogpost', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default=datetime.datetime(2013, 7, 22, 0, 0), unique=True, max_length=50),
                      keep_default=False)

        # Adding field 'BlogPost.published'
        db.add_column(u'blog_blogpost', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'BlogPost.url'
        raise RuntimeError("Cannot reverse this migration. 'BlogPost.url' and its values cannot be restored.")
        # Deleting field 'BlogPost.slug'
        db.delete_column(u'blog_blogpost', 'slug')

        # Deleting field 'BlogPost.published'
        db.delete_column(u'blog_blogpost', 'published')


    models = {
        u'blog.blogpost': {
            'Meta': {'object_name': 'BlogPost'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['blog']