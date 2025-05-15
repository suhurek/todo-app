from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="#4CAF50")  # カテゴリの色
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]
    
    REPEAT_CHOICES = [
        ('none', '繰り返しなし'),
        ('daily', '毎日'),
        ('weekly', '毎週'),
        ('monthly', '毎月'),
        ('custom', 'カスタム'),
    ]
    
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
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    # 繰り返し関連のフィールドを追加
    due_date = models.DateTimeField(null=True, blank=True)  # タスクの期日
    repeat_type = models.CharField(  # 繰り返しの種類
        max_length=10,
        choices=REPEAT_CHOICES,
        default='none'
    )
    repeat_interval = models.IntegerField(default=1)  # 繰り返し間隔（カスタム用）
    parent_task = models.ForeignKey(  # 親タスク（繰り返しで生成された場合）
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recurring_tasks'
    )
    
    def __str__(self):
        return self.title
    
    def create_next_occurrence(self):
        """完了時に次の繰り返しタスクを生成するメソッド"""
        if self.repeat_type == 'none' or not self.due_date:
            return None
            
        # 次の期日を計算
        next_due_date = None
        if self.repeat_type == 'daily':
            next_due_date = self.due_date + datetime.timedelta(days=self.repeat_interval)
        elif self.repeat_type == 'weekly':
            next_due_date = self.due_date + datetime.timedelta(weeks=self.repeat_interval)
        elif self.repeat_type == 'monthly':
            # 月の繰り返しは少し複雑
            month = self.due_date.month - 1 + self.repeat_interval
            year = self.due_date.year + month // 12
            month = month % 12 + 1
            day = min(self.due_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
            next_due_date = datetime.date(year, month, day)
        elif self.repeat_type == 'custom':
            next_due_date = self.due_date + datetime.timedelta(days=self.repeat_interval)
        
        if not next_due_date:
            return None
            
        # 次のタスクを作成
        new_task = Task.objects.create(
            title=self.title,
            description=self.description,
            category=self.category,
            priority=self.priority,
            due_date=next_due_date,
            repeat_type=self.repeat_type,
            repeat_interval=self.repeat_interval,
            parent_task=self.parent_task or self  # 親タスクが存在する場合はそれを使用、なければ自分自身
        )
        return new_task