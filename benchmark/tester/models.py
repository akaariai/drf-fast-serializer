from django.db import models
from datetime import date, datetime

class MyModel(models.Model):
    f1 = models.CharField(max_length=20)
    f2 = models.CharField(max_length=20)
    f3 = models.IntegerField()
    f4 = models.IntegerField()
    f5 = models.DateField()
    f6 = models.DateField()
    f7 = models.BooleanField(default=False)
    f8 = models.BooleanField(default=False)
    f9 = models.DateTimeField()
    f10 = models.DateTimeField()

    @classmethod
    def create(cls, i):
        MyModel(f1='asdf' * 5, f2='asdf' * 5,
                f3=i, f4=i, f5=date.today(), f6=date.today(),
                f7=True, f8=False, f9=datetime.now(), f10=datetime.now()).save()

class MySimpleModel(models.Model):
    f1 = models.CharField(max_length=20)
    f2 = models.CharField(max_length=20)

    @classmethod
    def create(cls, i):
        MySimpleModel(f1='asdf' * 5, f2='asdf' * 5).save()
