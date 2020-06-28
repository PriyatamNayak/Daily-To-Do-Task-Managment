from rest_framework import serializers
from projects.models import Activity ,TaskComment,ProjectTask
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

# Activity Serializer
'''
 Activity Creation for scheduled activity
 Activty Done button
'''
class ActivitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Activity 
    fields = ( 'Title', 'Description','status','scheduled','pk','parentActivityId')
    extra_kwargs = {'status': {'write_only': True}}
    def create(self, validated_data):
            '''
            Create ACtivity using Rest API
            '''
            act = Activity(
            Title=validated_data['Title'],
            Description=validated_data['Description'],
            Type=validated_data['Type'],parentActivityId=validated_data['parentActivityId']                     
            )
            act.save()
            return act
    def update(self, instance, validated_data):
            # Update Activity Status using Rest API
            instance.title = validated_data['status']
            instance.save()





# Notes Serializer
'''
api/revision/
api/revision/<int:pk>/
'''
class TaskCommentSerializer(TaggitSerializer,serializers.ModelSerializer):
  tags = TagListSerializerField()
  class Meta:
    model = TaskComment 
    fields = ('pk', 'content', 'updated','tags' ,'task')

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProjectTask 
    fields = '__all__'

  