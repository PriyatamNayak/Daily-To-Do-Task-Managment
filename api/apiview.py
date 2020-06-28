from rest_framework import viewsets
from projects.models import Activity,TaskComment,ProjectTask
from .serializers import ActivitySerializer,TaskCommentSerializer,TaskSerializer

class ActivityViewSet(viewsets.ModelViewSet):
        queryset = Activity.objects.all()
        serializer_class = ActivitySerializer


# We have seen 4 ways to build API views until now
# • Pure Django views
# • APIView subclasses
# • generics.* subclasses
# • viewsets.ModelViewSet
class TaskCommentViewSet(viewsets.ModelViewSet):
        queryset = TaskComment.objects.all()
        serializer_class = TaskCommentSerializer

class TaskViewSet(viewsets.ModelViewSet):
        queryset = ProjectTask.objects.all()
        serializer_class = TaskSerializer
