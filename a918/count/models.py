from django.db import models

# Create your models here.
class Shengfen(models.Model):
    shengfen_name = models.CharField(max_length=200)


class Daxue(models.Model):
    daxue_name = models.CharField(max_length=200)
    shengfen_id = models.IntegerField()


class Xsml(models.Model):
    Xsml_name = models.CharField(max_length=200)
    Xsml_bianhao = models.CharField(max_length=200)


class Xsxk(models.Model):
    Xsxk_name = models.CharField(max_length=200)
    Xsml_id = models.IntegerField()


class Zylx(models.Model):
    Zylx_name = models.CharField(max_length=200)
    Zylx_bianhao = models.CharField(max_length=200)


class Zyly(models.Model):
    Zyly_name = models.CharField(max_length=200)
    Zylx_id = models.IntegerField()


class Jilu(models.Model):
    Jilu_shengfen = models.CharField(max_length=200)
    Jilu_daxue = models.CharField(max_length=200)
    Jilu_type = models.CharField(max_length=20)
    #1 xs 2 zy
    Jilu_ml = models.CharField(max_length=200)
    Jilu_xk = models.CharField(max_length=200)
    Jilu_tp = models.CharField(max_length=20)


class wenjuan(models.Model):
    wenjuan_name = models.CharField(max_length=200)
    wenjuan_url = models.CharField(max_length=200)
    wenjuan_tuijian = models.CharField(max_length=10)
    wenjuan_status = models.IntegerField()