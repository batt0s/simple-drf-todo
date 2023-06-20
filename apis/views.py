from django.shortcuts import render

# Create your views here.

from todos.models import Todo
from apis.serializers import TodoSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class TodoList(APIView):
    """
    get: List all todos
    post: Create new todo
    """

    permission_classes=[IsAuthenticated] 
    
    def get(self, request):
        todos = Todo.objects.all().filter(owner=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["owner"] = request.user.id
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetail(APIView):
    """
    get: Get Todo
    put: Update Todo
    delete: Delete Todo
    """
    
    permission_classes=[IsAuthenticated] 

    def getTodo(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        todo = self.getTodo(pk)
        if todo.owner != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.getTodo(pk)
        if todo.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.getTodo(pk)
        if todo.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class RegisterUser(APIView):
    """
    post: Register a new user
    """
    def post(self, request):
        data = request.data
        user = User(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        user.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )
