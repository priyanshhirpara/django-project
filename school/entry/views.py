from entry.serializer import EntrySerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from entry.models import EntryModels
from competition.models import CompetitionModels
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.permission import AdminPermission , StudentPermission , TeacherPermission
from competition.serializer import CompetitionSerializer
from account.models import CustomUser
# Create your views here.
class CompetitionViewAll(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission|StudentPermission]
    def get(self,request: Request):
        if request.user.role == "admin" or "student":
            user = CompetitionModels.objects.all()
            serializer = CompetitionSerializer(user,many=True)
            return Response(serializer.data)


class EntryViewAll(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminPermission|TeacherPermission]
    def get(self,request: Request):
        user = CustomUser.objects.get(pk=request.user.id)
        if not  user:
            return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
        if request.user.role == "admin" or "teacher":
            user = EntryModels.objects.all()
            serializer = EntrySerializer(user,many=True)
            return Response(serializer.data)


class EntryView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [AdminPermission | StudentPermission ]
    def post(self, request: Request):
        user = CustomUser.objects.get(pk=request.user.id)
        if not  user:
            return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
        competition_id = request.data.get('competition')
        if not competition_id:
            return Response({'error': 'Competition ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comp = CompetitionModels.objects.get(id=competition_id)
        except CompetitionModels.DoesNotExist:
            return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            submission_date = serializer.validated_data.get('submission')
            if not submission_date:
                return Response({'error': 'Submission date is required'}, status=status.HTTP_400_BAD_REQUEST)
            if comp.start_date > submission_date:
                return Response({'error': 'This competition is not started yet'}, status=status.HTTP_409_CONFLICT)
            if comp.end_date < submission_date:
                return Response({'error': 'This competition is over now'}, status=status.HTTP_409_CONFLICT)
            serializer.save(user=request.user)
            return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data is saved'})
        return Response({'error': 'Validation error', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if not  user:
                return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
            entry = EntryModels.objects.get(pk=pk)
        except EntryModels.DoesNotExist:
            return Response({'error':'Entry is not found'})
        serializer = EntrySerializer(entry)
        return Response(serializer.data)
    
    def put(self,request:Request,pk):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if not  user:
                return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
            entry = EntryModels.objects.get(pk=pk)
        except EntryModels.DoesNotExist:
            return Response({'error':'Entry not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = EntrySerializer(entry,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if not  user:
                return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
            entry = EntryModels.objects.get(pk=pk)
        except EntryModels.DoesNotExist:
            return Response({'error':'Entry not found'},status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)