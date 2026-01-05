from django.db import models
# Create your models here.

# Relationships
# A Teacher teaches many Courses
# A Course has many Students
# A Student attends many Courses
# Attendance connects Student + Course + Date

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.IntegerField(unique=True)
    email = models.EmailField()
    dob = models.DateField()

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()  # Present or Absent

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"