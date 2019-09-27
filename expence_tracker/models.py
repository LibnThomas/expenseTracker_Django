from django.db import models
import datetime
from django.utils.timezone import now

# Create your models here.
class History(models.Model):
	item=models.CharField(max_length=10)
	price=models.IntegerField(max_length=10,default=0)
	p_date=models.DateField(default=datetime.date.today)
	p_time=models.TimeField(auto_now_add=True)
	uid=models.CharField(max_length=150)