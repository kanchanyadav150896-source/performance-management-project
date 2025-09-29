from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        # Placeholder login logic
        return Response({'token':'dummy-token'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        # Placeholder logout logic
        return Response({'message':'Logged out'}, status=status.HTTP_200_OK)
