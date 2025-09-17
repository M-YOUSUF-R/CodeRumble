from django.db import models

# Create your models here.
class Question(models.Model):
    CATEGORY_CHOICES = [
        ('math', 'Math'),
        ('dsa', 'DSA'),
        ('dp', 'DP'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField(default='question title')
    question = models.TextField()
    testcase = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.question[:30]}"
