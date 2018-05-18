from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InputSerializer, ResponseSerializer


import json
from .bot_response import response as response
# Create your views here.

class SendInputView(APIView):
    """This class defines the create behavior of our rest api."""
    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendResponseView(APIView):
    """This class defines the create behavior of our rest api."""
    def post(self, request, format=None):
        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class CreateUserView(APIView):
    """This class defines the create behavior of our rest api."""
    def post(self, request, format=None):
        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      


class GetResponse(APIView):
    """
    This function is used to contact the tensorflow model to generate automatic responses
    """
    def post(self, request, format=None):
        data = request.POST
        print("incoming message is: \n")
        print(data.get("msg"))
        response_msg = response(data.get("msg"))
        response_data = {
            "response": response_msg
        }
        return Response(response_data, status=status.HTTP_200_OK)         