from __future__ import unicode_literals

from django.db import models

# Create your models here.
class IMUser(models.Model):
    userid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, default='')
    wechatid = models.CharField(max_length=100, blank=True, default='')
    photo = models.CharField(max_length=100, blank=True, default='')
    bgimg = models.CharField(max_length=100, blank=True, default='')
    note = models.CharField(max_length=100, blank=True, default='')
    token = models.CharField(max_length=100, blank=True, default='')
    rctoken = models.CharField(max_length=100, blank=True, default='')
    friends = models.ManyToManyField("self", blank=True)

    @property
    def friendlist(self):
        # Watch for large querysets: it loads everything in memory
        return list(self.friends.all())
    def __unicode__(self):
        return self.name
    def image_tag(self):
        return u'<img src="%s" width="40" height="40">' % (self.photo)
    image_tag.short_description = 'Thumb'
    image_tag.allow_tags = True

class FriendShip(models.Model):
	fsid = models.AutoField(primary_key=True, default='1')
	fromid = models.ForeignKey('IMUser', related_name='friendship_requests_sent')
	toid = models.ForeignKey('IMUser', related_name='friendship_requests_receive')