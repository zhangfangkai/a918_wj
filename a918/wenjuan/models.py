from django.db import models

# Create your models here.
class Wenjuan(models.Model):
    user_id = models.IntegerField()
    wenjuan_name = models.CharField(max_length=200)


class Wenti(models.Model):
    wenti_name = models.CharField(max_length=200)
    wenjuan_id = models.IntegerField()
    wenti_type = models.IntegerField()
    wenti_xuhao = models.IntegerField()


class Xuanxiang(models.Model):
    wenti_id = models.IntegerField()
    xuanxiang_name = models.CharField(max_length=200)
    xuanxiang_xuhao = models.IntegerField()


class Huida(models.Model):
    wenjuan_id = models.IntegerField()
    wenti_id = models.IntegerField()
    huida_data = models.CharField(max_length=1000)
    huida_tip = models.CharField(max_length=64)

