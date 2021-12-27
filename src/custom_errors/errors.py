from rest_framework.response import Response
from rest_framework import status

def profileError():
  return Response({'message' : 'User needs to create a profile first'}, status=status.HTTP_403_FORBIDDEN)

def unauthorized_access_error():
  return Response({'message' : 'User is unauthorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)