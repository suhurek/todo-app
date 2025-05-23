from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'created_at']
        
class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    parent_task_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'completed', 'created_at', 
            'updated_at', 'category', 'category_id', 'priority',
            'due_date', 'repeat_type', 'repeat_interval', 'parent_task_id'
        ]

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        parent_task_id = validated_data.pop('parent_task_id', None)
        
        task = Task.objects.create(**validated_data)
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                task.category = category
                task.save()
            except Category.DoesNotExist:
                pass
                
        if parent_task_id:
            try:
                parent_task = Task.objects.get(id=parent_task_id)
                task.parent_task = parent_task
                task.save()
            except Task.DoesNotExist:
                pass
                
        return task

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        parent_task_id = validated_data.pop('parent_task_id', None)
        
        instance = super().update(instance, validated_data)
        
        if category_id is not None:
            try:
                if category_id:
                    category = Category.objects.get(id=category_id)
                    instance.category = category
                else:
                    instance.category = None
                instance.save()
            except Category.DoesNotExist:
                pass
                
        if parent_task_id is not None:
            try:
                if parent_task_id:
                    parent_task = Task.objects.get(id=parent_task_id)
                    instance.parent_task = parent_task
                else:
                    instance.parent_task = None
                instance.save()
            except Task.DoesNotExist:
                pass
                
        return instance