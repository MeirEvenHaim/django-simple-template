from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.shortcuts import get_object_or_404
from .models import Sloves
from .serializers import SlovesSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 


#this is my register endpoint we create it using methodes and decorator andnot classes from simplicity sake 
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request) : 
    username = request.data.get('username') #recives the inputs of the credentials username and password and saves them inside the data of the User table as a user 
    password = request.data.get('password')

    if not username or not password :
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
       return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)# this checks wethere the usename and password already exists within the db so theere wont be duplicated users.
   
    user = User.objects.create_user(username=username, password=password) #create_user is a built in function to create and register new users into User db and applying the value of your password and username inputs into the db as passwords and username 
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


# Login user and obtain JWT token
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = get_object_or_404(User, username=username)

    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)
    

# List and Create Sloves
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) # if user is autheticated with acces token he will be able to see all products of the slaves and even add new slaves to the database
def sloves_list_create(request):
    if request.method == 'GET':#responsible for the viewing allow us the display the data within the db 
        sloves = Sloves.objects.all()#takes the Slove class and all of its objects and applying it to the vlaue of the sloves variable 
        serializer = SlovesSerializer(sloves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':# created a new slove instance using post http methode 
        serializer = SlovesSerializer(data=request.data)
        if serializer.is_valid(): # check if the serializer is corrected will give a new slave to the db 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update, Delete Sloves
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def sloves_detail(request, pk):
    sloves = get_object_or_404(Sloves, pk=pk)# shows you the data by its id / pk 

    if request.method == 'GET':
        serializer = SlovesSerializer(sloves) #takes the request from the get_object_or_404 and validates if the request is sent correctly 
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = SlovesSerializer(sloves, data=request.data) # an update method that checks if the updated data is being sent in the corrected format and then saves it using a serializer method save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        sloves.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)