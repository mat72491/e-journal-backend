from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JournalEntry, Tag
from .serializers import EntrySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import Tag
from django.db.models import Count
# Create your views here.

#Get Request
class EntryListView(APIView):
    def get(self, request):
        entries = JournalEntry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# POST request 
class EntryCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUT request 
class EntryUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            entry = JournalEntry.objects.get(pk=pk)
            print(entry)
            print(request.data)
        except JournalEntry.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EntrySerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE request 
class EntryDeleteView(APIView):
    def delete(self, request, pk):
        try:
            entry = JournalEntry.objects.get(pk=pk)
        except JournalEntry.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# User Registration View
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login/Authentication View
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class JournalEntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user)
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

class JournalEntryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            entry = JournalEntry.objects.get(pk=pk, user=request.user)
            serializer = EntrySerializer(entry)
            return Response(serializer.data)
        except JournalEntry.DoesNotExist:
            return Response({"detail": "Entry not found."}, status=404)

class JournalEntryEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            entry = JournalEntry.objects.get(pk=pk, user=request.user)
            serializer = EntrySerializer(entry, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except JournalEntry.DoesNotExist:
            return Response({"detail": "Entry not found."}, status=404)


class JournalEntryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            entry = JournalEntry.objects.get(pk=pk, user=request.user)
            entry.delete()
            return Response({"detail": "Entry deleted successfully."}, status=204)
        except JournalEntry.DoesNotExist:
            return Response({"detail": "Entry not found."}, status=404)

@api_view(['GET'])
def get_entries_count(request):
    if request.user.is_authenticated:
        count = JournalEntry.objects.filter(user=request.user).count()
        return Response({'count': count})
    return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

@api_view(['GET'])
def get_tags(request):
    tags = Tag.objects.all()
    tag_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return Response(tag_list)

@api_view(['GET'])
def get_top_tags(request):
    if request.user.is_authenticated:
        top_tags = Tag.objects.annotate(num_entries=Count('journal_entries')).order_by('-num_entries')[:3]
        tags = [{'id': tag.id, 'name': tag.name, 'count': tag.num_entries} for tag in top_tags]
        return Response(tags)
    return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

@api_view(['GET'])
def get_recent_entries(request):
    if request.user.is_authenticated:
        recent_entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:3]
        entries = [{'id': entry.user.username, 'title': entry.title, 'created_at': entry.created_at, 'entry': entry.content} for entry in recent_entries]
        return Response(entries)
    return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

@api_view(['POST'])
def create_journal_entry(request):
    if request.user.is_authenticated:
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    return Response({'detail': 'Authentication credentials were not provided.'}, status=401)


