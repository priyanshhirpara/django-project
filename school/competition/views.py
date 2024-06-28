from competition.serializer import CompetitionSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from competition.models import CompetitionModels
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.permission import AdminPermission , TeacherPermission
from account.models import CustomUser
# Create your views here.

class CompetitionViewAll(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission]
    def get(self,request: Request):
        if request.user.role == "admin" or "teacher":
            user = CompetitionModels.objects.all()
            serializer = CompetitionSerializer(user,many=True)
            return Response(serializer.data)

class CompetitionViews(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission]
    def post(self,request:Request):
        user = CustomUser.objects.get(pk=request.user.id)
        if not  user:
            return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CompetitionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':403,'error':serializer.errors,'message':'something went wrong'})
        serializer.save(user=request.user)
        return Response({'status':200,'payload':serializer.data,'message':'your data is saved'})

    def get(self,request,pk):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if not  user:
                return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
            competition = CompetitionModels.objects.get(pk=pk)
        except CompetitionModels.DoesNotExist:
            return Response({'error':'Competition is not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data)
    
    def put(self,request:Request,pk):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if not  user:
                return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
            competition = CompetitionModels.objects.get(pk=pk)
        except CompetitionModels.DoesNotExist:
            return Response({'error':'Competition not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CompetitionSerializer(competition,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if not  user:
                return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
            competition = CompetitionModels.objects.get(pk=pk)
        except CompetitionModels.DoesNotExist:
            return Response({'error':'Competition not found'},status=status.HTTP_404_NOT_FOUND)
        competition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)