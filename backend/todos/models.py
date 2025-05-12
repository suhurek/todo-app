from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="#4CAF50")  # カテゴリの色
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tasks'
    )
    
    def __str__(self):
        return self.title