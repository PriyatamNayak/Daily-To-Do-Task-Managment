from django.shortcuts import render
from projects.models import Activity,TaskComment,ProjectTask
from .serializers import ActivitySerializer,TaskCommentSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template import loader
from datetime import datetime

# URLS 
# (option)http://localhost:8000/api/activities/
# (GET)http://localhost:8000/api/activities/
# (Get)http://localhost:8000/api/activities/1/
# Create your views here.
class ActivityList(APIView):
        def get(self, request):
            records = Activity.objects.all()
            data = ActivitySerializer(records, many=True).data
            return Response(data)
class ActivityDone(APIView):
    '''
    API for make activity done. 
    There would be button on Activity to make it done.
    '''
    def get(self, request, pk):
        record = get_object_or_404(Activity, pk=pk)
        Act = Activity.objects.get(pk=pk)
        Act.status="Done"
        Act.save()   
        return Response(Act.status)

class ScheduledActivityList(APIView):
        '''
        get all scheduled activity to create daily activities.
        '''
        def get(self, request):
            records = Activity.objects.exclude(Type="General")
            data = ActivitySerializer(records, many=True).data
            return Response(data)

class ActivityDetail(APIView):
    def get(self, request, pk):
        record = get_object_or_404(Activity, pk=pk)
        data = ActivitySerializer(record).data
        return Response(data)

class RevisionItem(APIView):
    def get(self, request):
        records = TaskComment.objects.all().order_by('updated')[1]
        data = TaskCommentSerializer(records).data
        return Response(data)

class RevisionItemUpdate(APIView):
    def get(self, request,pk):
        comment = TaskComment.objects.get(pk=pk)
        comment.updated=timezone.now()
        comment.save()
        return Response("Success")

class RevisionItemofTheDay(APIView):
    def get(self, request):
        dt = datetime.now()
        queryset = Activity.objects.filter(scheduled__lte=dt,Type='General').exclude(status='Done').order_by('-scheduled')            
        html_message = loader.render_to_string('api/mail_template.html', {'Activities': queryset})
        email = EmailMessage('Task of the day', html_message,to=['mailtodanish@gmail.com'])
        email.content_subtype = "html" 
        email.send()   
        return Response("Success")
# The generic views of Django Rest Framework help us in code reusablity. 

class all_task(APIView):
    # All task API
    def get(self, request):
        records = ProjectTask.objects.all()
        data = TaskSerializer(records, many=True).data
        return Response(data)

class all_task_items(APIView):
    # All task API
    def get(self, request, pk):
        records = TaskComment.objects.filter(task=pk).order_by('updated')
        data  = TaskCommentSerializer(records, many=True).data
        return Response(data)




