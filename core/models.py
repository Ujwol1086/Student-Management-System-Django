from django.db import models
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField(max_length=20, unique=True)
    email = models.EmailField()
    dob = models.DateField()

    def __str__(self):
        return self.name
    