from rest_framework import generics
from projects.models import Activity
from .serializers import ActivitySerializer

# Using DRF generic views to simplify code
class ActivityListGeneric(generics.ListCreateAPIView):
        queryset = Activity.objects.all()
        serializer_class = ActivitySerializer

class ActivityDetailGeneric(generics.RetrieveDestroyAPIView):
        def get_queryset(self):
            queryset = Activity.objects.filter(pk=self.kwargs["pk"])
            return queryset
        serializer_class = ActivitySerializer

class ActivityCreate(generics.CreateAPIView):
         serializer_class = ActivitySerializer

'''
# OPTIONS gives more detail when using generic
This tells us
• Our API now accepts POST
• The required data fields
• The type of each data field.
{
    "name": "Activity List Generic",
    "description": "",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "id": {
                "type": "integer",
                "required": false,
                "read_only": true,
                "label": "ID"
            },
            "Title": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Title",
                "max_length": 200
            },
            "Description": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Description"
            },
            "created": {
                "type": "datetime",
                "required": false,
                "read_only": true,
                "label": "Created"
            },
            "status": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Status",
                "max_length": 100
            },
            "Type": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Type",
                "max_length": 100
            },
            "scheduled": {
                "type": "datetime",
                "required": false,
                "read_only": false,
                "label": "Scheduled"
            },
            "updated": {
                "type": "datetime",
                "required": false,
                "read_only": false,
                "label": "Updated"
            }
        }
    }
} 

The /activity/ and /activity/<pk>/ urls require two view classes, with the same serializer and base queryset. We
can group them into a viewset, and connect them to the urls using a router.
'''
