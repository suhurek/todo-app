from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    
    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        completed = request.data.get('completed', not task.completed)
        task.completed = completed
        task.save()
        
        # 繰り返しタスクの処理
        new_task = None
        if completed and task.repeat_type != 'none':
            new_task = task.create_next_occurrence()
            
        serializer = self.get_serializer(task)
        response_data = serializer.data
        
        # 新しいタスクが生成された場合、レスポンスに追加
        if new_task:
            new_task_serializer = self.get_serializer(new_task)
            response_data['next_task'] = new_task_serializer.data
            
        return Response(response_data)
    
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        task_orders = request.data.get('task_orders', [])
        for task_order in task_orders:
            task_id = task_order.get('id')
            new_order = task_order.get('order')
            if task_id and new_order is not None:
                Task.objects.filter(id=task_id).update(order=new_order)
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # 総タスク数と完了/未完了の割合
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(completed=True).count()
        
        # カテゴリ別のタスク数
        category_distribution = []
        categories = Category.objects.all()
        for category in categories:
            count = Task.objects.filter(category=category).count()
            category_distribution.append({
                'name': category.name,
                'color': category.color,
                'count': count
            })
        
        # カテゴリなしのタスク数も追加
        category_none_count = Task.objects.filter(category=None).count()
        if category_none_count > 0:
            category_distribution.append({
                'name': 'カテゴリなし',
                'color': '#CCCCCC',
                'count': category_none_count
            })
        
        # 優先度別のタスク数
        priority_counts = Task.objects.values('priority').annotate(count=Count('id'))
        priority_distribution = {}
        for item in priority_counts:
            priority_distribution[item['priority']] = item['count']
        
        # 最近7日間の日ごとの完了タスク数
        today = timezone.now().date()
        daily_completion = []
        
        for i in range(6, -1, -1):  # 6日前から今日まで
            day = today - timedelta(days=i)
            count = Task.objects.filter(
                completed=True, 
                updated_at__date=day
            ).count()
            daily_completion.append({
                'date': day.strftime('%Y-%m-%d'),
                'day': day.strftime('%m/%d'),
                'count': count
            })
        
        return Response({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completed_tasks / total_tasks if total_tasks > 0 else 0,
            'category_distribution': category_distribution,
            'priority_distribution': priority_distribution,
            'daily_completion': daily_completion
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer