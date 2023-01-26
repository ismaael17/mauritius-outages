from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100)
    
class Outage(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    location = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    



# Create your models here.