# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class EngineCount(models.Model):
    ask = models.IntegerField()
    yahoo = models.IntegerField()
    bing = models.IntegerField()
    google = models.IntegerField()
    google2 = models.IntegerField()
    class Meta:
        db_table = 'enginecount'


class DataTable(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2550, blank=True, null=True)
    mail = models.CharField(max_length=2550, blank=True, null=True)
    creattime = models.DateTimeField(blank=True, null=True)
    kw = models.ForeignKey('KeywordTable', models.DO_NOTHING, blank=True, null=True)
    remark1 = models.CharField(max_length=2550, blank=True, null=True)
    remark2 = models.CharField(max_length=2550, blank=True, null=True)
    remark3 = models.CharField(max_length=2550, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_table'


class KeywordTable(models.Model):
    keyword = models.CharField(max_length=255)
    googleind = models.IntegerField(blank=True, null=True)
    askind = models.IntegerField(blank=True, null=True)
    bingind = models.IntegerField(blank=True, null=True)
    updatetime = models.DateTimeField()
    remark = models.CharField(max_length=255, blank=True, null=True)
    remark2 = models.CharField(max_length=255, blank=True, null=True)
    remark3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keyword_table'
