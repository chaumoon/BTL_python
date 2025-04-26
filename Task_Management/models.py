from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Account'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Tag'
        
class Task(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dl = models.DateTimeField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    des = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Task'
