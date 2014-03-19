from django.db import models

# Create your models here.
class Coupon(models.Model):
	title=models.CharField(max_length=50, null=True)
	description=models.TextField(max_length=500, null=True)
	location=models.CharField(max_length=100, null=True)
	price=models.DecimalField(max_digits=4, decimal_places=0)



class Challenge(models.Model):
	title=models.CharField(max_length=50, null=True)
	description=models.TextField(max_length=500, null=True)
	location=models.CharField(max_length=100, null=True)
	points=models.DecimalField(max_digits=4, decimal_places=0)	