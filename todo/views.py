from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status

# Create your views here.
class TodoCreateRetrieve(APIView):
    """ View to list all and create todo in the system.

    * Requires token authentication.
    * Only logged in users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        todos = Todo.objects.filter(user = request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class TodoDetails(APIView):
    """ View to get, update and delete a single todo in the system

    * Requires token authentication.
    * Only logged in users are able to access this view.    
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, id):
        todo = Todo.objects.get(id = id)
        if todo.user == request.user:
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(data = {"error":"Unauthorised"}, status = status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, id):
        todo = Todo.objects.get(id = id)
        serializer = TodoSerializer(todo, data = request.data)
        if todo.user == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data = {"error":"Unauthorised"}, status = status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, id):
        todo = Todo.objects.get(id = id)
        if todo.user == request.user:
            todo.delete()
            return Response(data = {"message":"delete successs"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data = {"error":"Unauthorised"}, status = status.HTTP_401_UNAUTHORIZED)
        
        
    
    
    
    