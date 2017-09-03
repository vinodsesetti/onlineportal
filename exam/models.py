from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
#from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
# Create your models here.
from django.conf import settings

class Exam(models.Model):
    exam_name = models.CharField(max_length=50)
    duration = models.DurationField(default=timedelta(minutes=40))
    date_published = models.DateField()
    branch = models.CharField(max_length=250,blank=True)
    def __str__(self):
        return self.exam_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=100, verbose_name='option1', default='none')
    option2 = models.CharField(max_length=100, verbose_name='option2', default='none')
    option3 = models.CharField(max_length=100, verbose_name='option3', default='none')
    option4 = models.CharField(max_length=100, verbose_name='option4', default='none')
    answer = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(4), MinValueValidator(1)])

    def __str__(self):
        return 'Question:' + self.question_text

# class Question(models.Model):
#     question_text = RichTextField()
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     option1 = RichTextField()
#     option2 = RichTextField()
#     option3 = RichTextField()
#     option4 = RichTextField()
#     answer = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(4), MinValueValidator(1)])

#     def __str__(self):
#         return 'Question:' + self.question_text



class Profile(AbstractUser):
   number = models.IntegerField(null=True,default="999999999")
   branch=models.CharField(max_length = 50)
   year=models.CharField(max_length = 50)
   image = models.ImageField(upload_to = 'images/')

 
class Report(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return ' User :' + self.user.username + 'Exam :' + self.exam.exam_name + 'marks:' + str(self.marks)


class Results(models.Model):
   marks = models.IntegerField(blank=True,null=True)
   name=models.CharField(max_length = 300)
   year=models.CharField(max_length = 50)
   branch=models.CharField(max_length = 50)

