from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
# Create your models here.

from base_manager import BaseManager

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    tshow = models.CharField(max_length=20, default='')
    tbanner = models.ImageField(upload_to='images')

    tcommend1 = models.ForeignKey("GoodsInfo", related_name='commend1', blank=True, null=True)
    tcommend2 = models.ForeignKey("GoodsInfo", related_name='commend2', blank=True, null=True)
    tcommend3 = models.ForeignKey("GoodsInfo", related_name='commend3', blank=True, null=True)

    isDelete = models.BooleanField(default=False)

    objects = BaseManager()
    old_objects = models.Manager()

    def __str__(self):
        return self.ttitle


class TagInfo(models.Model):
    tname = models.CharField(max_length=20, unique=True)
    ttime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tname


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField(default=0)
    gsummary = models.CharField(max_length=256)
    gstorage = models.IntegerField()
    gwarning = models.IntegerField(default=50)
    gcontent = HTMLField()
    gbig_pic = models.ImageField(upload_to='df_goods')
    up_time = models.DateField(auto_now_add=True)

    isDelete = models.BooleanField(default=False)

    gtype = models.ForeignKey("TypeInfo")
    gtags = models.ManyToManyField('TagInfo', blank=True)


    objects = BaseManager()
    old_objects = models.Manager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.gtitle


class Slide(models.Model):
    stitle = models.CharField(max_length=100, blank=True, null=True)
    salt = models.CharField(max_length=100, blank=True, null=True)
    spic = models.ImageField(upload_to='images')
    goods = models.ForeignKey("GoodsInfo", null=True)

    def __str__(self):
        return self.goods

class Adv(models.Model):
    atitle = models.CharField(max_length=100, blank=True, null=True)
    aalt = models.CharField(max_length=100, blank=True, null=True)
    apic = models.ImageField(upload_to='images')
    goods = models.ForeignKey("GoodsInfo", null=True)

    def __str__(self):
        return self.goods