from rest_framework import serializers
from todos import models
from django.contrib.auth.models import User


class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=64)
    description = serializers.CharField(required=True, allow_blank=False, max_length=256)
    done = serializers.BooleanField(default=False)
    owner = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all(), required=False)

    def create(self, validated_data):
        return models.Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Todo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'todos']
