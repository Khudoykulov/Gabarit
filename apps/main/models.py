from django.db import models

# Create your models here.


class Gabarit(models.Model):
    name = models.CharField(max_length=123,default='BMW')
    width = models.IntegerField()
    length = models.IntegerField()
    high = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



