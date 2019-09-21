from django.db import models

# Create your models here.
class History(models.Model):
	item=models.CharField(max_length=10)
	price=models.IntegerField(max_length=10,default=0)

class db_login(models.Model):
	uname=models.CharField(max_length=10)
	upass=models.CharField(max_length=15)
		