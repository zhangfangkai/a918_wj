# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=50)
    user_password = models.CharField(max_length=20, blank=True)


# zfk
class Wenjuan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wj_name = models.CharField(max_length=100)
    wj_date = models.DateTimeField('date created', auto_now=True)


class Questype(models.Model):
    ques_type = models.CharField(max_length=20)


class Question(models.Model):
    questype = models.ForeignKey(Questype, on_delete=models.CASCADE)
    wenjuan = models.ForeignKey(Wenjuan, on_delete=models.CASCADE)
    q_con = models.CharField(max_length=200)
    q_xuhao = models.CharField(max_length=200)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    cho_num = models.CharField(max_length=10)
    cho_con = models.CharField(max_length=200)


class Score(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    cho_num = models.CharField(max_length=10)
    score_con = models.CharField(max_length=200)


class Record(models.Model):
    wenjuan = models.ForeignKey(Wenjuan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ans_data = models.DateTimeField('date answered', auto_now=True)


class Ans_choice(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


class Ans_wenda(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans_con = models.CharField(max_length=200)


# ---zfk add on 2017-08-31
class Ans_score(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    scores = models.IntegerField()
    score = models.ForeignKey(Score, on_delete=models.CASCADE)


class City(models.Model):
    city_xuhao = models.IntegerField()
    city_name = models.CharField(max_length=30)


class University(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    univers_xuhao = models.IntegerField()
    univers_name = models.CharField(max_length=100)

class Xuewei(models.Model):
    xuewei_xuhao = models.IntegerField()
    xuewei_name = models.CharField(max_length=100)

# ---


