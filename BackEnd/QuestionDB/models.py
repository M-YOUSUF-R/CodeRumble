from django.db import models

# Create your models here.
class Question(models.Model):
    CATEGORY_CHOICES = [
        ('math', 'Math'),
        ('dsa', 'DSA'),
        ('dp', 'DP'),
    ]
    q_category = models.CharField(max_length=10)
    q_title = models.CharField(max_length=200,default='question title')
    question = models.TextField()
    q_testcase = models.TextField()
    q_answer = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.question[:30]}"
