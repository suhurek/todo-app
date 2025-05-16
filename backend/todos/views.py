from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer