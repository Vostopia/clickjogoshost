import os
from django.db import models
from django.utils.datetime_safe import strftime
from django.utils.timezone import now
import shortuuid

from ..s3direct.fields import S3DirectField
from django.conf import settings


class WebPlayerManager(models.Manager):
    def get_active(self):
        """
        Get the active WebPlayer object
        """
        #find or create an active webplayer
        actives = ActiveWebPlayer.objects.all()
        if len(actives) > 0:
            active = actives[0]
        else:
            active = ActiveWebPlayer()
            active.save()

        #if more than one active, delete the others
        if len(actives) > 1:
            for a in actives[1:]:
                a.delete()

        #get webplayer object from active
        webplayer = active.webplayer

        #if active does not have a webplayer set, set the first and best webplayer
        if not webplayer:
            webplayers = WebPlayer.objects.all()
            if len(webplayers) > 0:
                webplayer = webplayers[0]
                active.webplayer = webplayer
                active.save()

        return webplayer


def _upload_to(webplayer, original_filename):
    return _upload_to_prefix(webplayer, original_filename, "webplayer")


def _upload_to_logo(webplayer, original_filename):
    return _upload_to_prefix(webplayer, original_filename, "webplayer/logo")


def _upload_to_progressbar(webplayer, original_filename):
    return _upload_to_prefix(webplayer, original_filename, "webplayer/progressbar")


def _upload_to_progressbarframe(webplayer, original_filename):
    return _upload_to_prefix(webplayer, original_filename, "webplayer/progressbarframe")


def _upload_to_notloggedin(webplayer, original_filename):
    return _upload_to_prefix(webplayer, original_filename, "webplayer/notloggedin")


def _upload_to_prefix(webplayer, original_filename, prefix):
    basename = os.path.basename(original_filename)
    name, ext = os.path.splitext(basename)
    uuid = shortuuid.uuid()
    datepart = strftime(now(), "%Y-%m-%d")
    return "%s/%s-%s-%s%s" % (prefix, name, datepart, uuid, ext)


class WebPlayer(models.Model):
    """
    Represents an uploaded unity webplayer. File should never change,
    rather a new WebPlayer should be created, and ActiveWebPlayer should
    be set to point to the new WebPlayer
    """
    name = models.CharField(blank=False, default="Webplayer", max_length=255)
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=575)
    backgroundcolor = models.CharField(default="FFFFFF", max_length=16)
    bordercolor = models.CharField(default="FFFFFF", max_length=16)
    textcolor = models.CharField(default="000000", max_length=16)

    if settings.USE_S3_STORAGE:
        file = S3DirectField(upload_to=os.path.join(settings.S3DIRECT_DIR, "webplayer"))
        logo_image = S3DirectField(upload_to=os.path.join(settings.S3DIRECT_DIR, "webplayer/logo"), blank=True)
        progressbar_image = S3DirectField(upload_to=os.path.join(settings.S3DIRECT_DIR, "webplayer/progressbar"), blank=True)
        progressbarframe_image = S3DirectField(upload_to=os.path.join(settings.S3DIRECT_DIR, "webplayer/progressbareframe"), blank=True)
        notloggedin_image = S3DirectField(upload_to=os.path.join(settings.S3DIRECT_DIR, "webplayer/notloggedin"), blank=True, default="")

    else:
        file = models.FileField(upload_to=_upload_to)
        logo_image = models.FileField(upload_to=_upload_to_logo, blank=True)
        progressbar_image = models.FileField(upload_to=_upload_to_progressbar, blank=True)
        progressbarframe_image = models.FileField(upload_to=_upload_to_progressbarframe, blank=True)
        notloggedin_image = models.FileField(upload_to=_upload_to_notloggedin, blank=True, default="")

    #custom manager
    objects = WebPlayerManager()

    def __unicode__(self):
        return self.name


class ActiveWebPlayer(models.Model):
    """
    Points to the active webplayer. Only one row should exist in this table
    """
    webplayer = models.ForeignKey(WebPlayer, null=True)