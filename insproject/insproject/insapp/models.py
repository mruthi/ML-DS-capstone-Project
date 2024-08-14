from django.db import models

# Create your models here.
class insModel(models.Model):

    age=models.IntField()
    bmi=models.FloatField()
    children=models.IntField()
    sex_male=models.FloatField()
    smoker_yes=models.FloatField()
