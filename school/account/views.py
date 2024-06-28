from account.serializer import UserProfileSerializer, ShowSerializer
from rest_framework import  request ,response ,status
from account.models import CustomUser
from rest_framework.views import APIView
from account.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.permission import AdminPermission ,TeacherPermission , StudentPermission
from rest_framework.permissions import AllowAny
# Create your views here.

def create_token(user):
    token = RefreshToken.for_user(user)
    refresh = str(token)
    access = str(token.access_token)
    response_data = {
        "id": user.id,
        "email": user.email,
        "access": access,
        "refresh": refresh,
    }
    return response_data

class Userprofile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self,request:request.Request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = create_token(user)
            return response.Response(token, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self,request:request.Request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return response.Response('Incorrect Credentials',status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return response.Response('Incorrect Password',status=status.HTTP_401_UNAUTHORIZED)
        token = create_token(user)
        return response.Response(token,status=status.HTTP_200_OK)       

class StudentAllData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission]
    def get(self,request):
        if request.user.role == "admin" or "teacher":
            user = CustomUser.objects.filter(role="student")
            serializer = ShowSerializer(user,many=True)
            return response.Response(serializer.data)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        
class StudentIDData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission]
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return response.Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        if user.role == "teacher" or user.role == "admin":
            return response.Response({"error":"You have no access"},status=status.HTTP_401_UNAUTHORIZED)
        serializer = ShowSerializer(user)
        return response.Response(serializer.data)

class TeachersAllData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission]
    def get(self,request):
        if request.user.role == "admin":
            user = CustomUser.objects.filter(role="teacher")
            serializer = ShowSerializer(user,many=True)
            return response.Response(serializer.data)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

class TeacherIDData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission]
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return response.Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        if user.role == "student" or user.role == "admin":
            return response.Response({"error":"You have no access"},status=status.HTTP_401_UNAUTHORIZED)
        serializer = ShowSerializer(user)
        return response.Response(serializer.data)

class Userviews(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission|StudentPermission]
    def patch(self,request:request.Request):
        try:
            user = CustomUser.objects.get(pk = request.user.id)
        except CustomUser.DoesNotExist:
            return response.Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request:request.Request): 
        try:
            user = CustomUser.objects.get(pk=request.user.id)
        except CustomUser.DoesNotExist:
            return response.Response({'error':'User not found '},status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return response.Response({'error':'Your user delete'},status=status.HTTP_204_NO_CONTENT)

class MeViews(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission|StudentPermission]
    def get(self,request):
        user = CustomUser.objects.get(pk=request.user.id)
        serializer = ShowSerializer(user)
        return response.Response(serializer.data)