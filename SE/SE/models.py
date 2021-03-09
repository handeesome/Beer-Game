#Import the django models library
from django.db import models

'''
This class corresponds to the 'User' table in the database.
It defines the same attributes that are in the database table.
'''
class Instructor_Registration(models.Model):
	FirstName = models.CharField(max_length=150)
	LastName = models.CharField(max_length=150)
	Email = models.CharField(max_length=150)
	Password = models.CharField(max_length=150)
	class Meta:
		db_table = "User"
