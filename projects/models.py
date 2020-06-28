from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django_cryptography.fields import encrypt
from django.core.signing import Signer
from django.utils.text import slugify
from unidecode import unidecode
from django.utils.html import mark_safe

class ApplictaionData(models.Model):
        '''
        It will store applictaion related data 
        static list of value
        '''
        Name = models.CharField(max_length=200,null = False)
        Value = models.CharField(max_length=200, null = False)        
        IsCategory = models.BooleanField(null=True) 
        Type = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
        Description =models.CharField(max_length=200,null = False)
        def get_absolute_url(self):
              return reverse('lov-view')        
        def __str__(self):
            return self.Name

def generate_unique_slug(_class, field):    
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while _class.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

class ProjectTask(models.Model):
        '''
        It will store major task and related info as comment and timeline
        '''       
        Task_Description =models.CharField(max_length=200,null = False,unique=True)
        Task_Title = models.TextField(null = False,unique=True)
        created = models.DateTimeField(auto_now_add=True) 
        signer = Signer(salt='projectTask.Task')
        slug = models.SlugField(max_length=200, unique=True,null = True)
        

        def __str__(self):
            return self.Task_Title        

        def get_signed_hash(self):
          signed_pk = self.signer.sign(self.slug)
          return signed_pk

        def get_absolute_url(self):
            return reverse('shared-task-detail', args=(self.get_signed_hash(),))

        def save(self, *args, **kwargs):
          Task_Title = unidecode(self.Task_Title)
          if self.slug:
              if slugify(Task_Title) != self.slug:
                  self.slug = generate_unique_slug(ProjectTask, Task_Title)
          else:
              self.slug = generate_unique_slug(ProjectTask, Task_Title)
          super().save(*args, **kwargs)
       

class TaskComment(models.Model) :
            '''
            It will store task related data 
            and timeline
            '''
            content = encrypt(HTMLField(null = True))
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(default=timezone.now)
            tags = TaggableManager(blank=True)
            signer = Signer(salt='projectTask.Task')
            task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE,blank=True, null=True)
            
            def get_signed_hash(self):
                  signed_pk = self.signer.sign(self.task.slug)
                  return signed_pk

            def get_absolute_url(self):
                  return reverse('task-detail', args=(self.get_signed_hash(),))

              

class FavLink(models.Model) :
            '''
            Favourite link
            
            '''
            name =models.CharField(max_length=200,null = False,unique=True)
            link =models.CharField(max_length=200,default="no link")
            created = models.DateTimeField(auto_now_add=True)     
            def __str__(self):
                     return self.name

class Activity(models.Model) :
            '''
            Activities
            
            '''
            Title =models.CharField(max_length=200,null = False,unique=True)
            Description =models.TextField()
            created = models.DateTimeField(auto_now_add=True)
            status = models.CharField(max_length=100,default='Open')
            Type=  models.CharField(max_length=100, default='General', null=True) 
            scheduled = models.DateTimeField(default=timezone.now, null=True)
            #updated at and it will be popuplated on save()
            updated = models.DateTimeField(default=timezone.now)
            # stores id of parent activity for scheduled activity.
            parentActivityId=models.IntegerField(null = True,unique=False,default=0)

            @property
            def isScheduled(self):
              '''
               property : if scheduled activity is scheduled or have past date.
              '''
              if self.Type != "General":
                    if timezone.localtime() > timezone.localtime(self.scheduled) :                      
                      return True
                    else:
                      return False
              else:
                return False
                    
            def __str__(self):
                     return self.Title

            def get_absolute_url(self):
              return reverse('activity-detail', args=[self.pk])
            
            def one_day_hence(self):
                    return timezone.now() + timezone.timedelta(days=1)

            def save(self, *args, **kwargs):
                self.updated=timezone.now()
                super().save(*args, **kwargs)
                if self.status == "Done" and self.parentActivityId != 0:
                    #search activity and update rescheduled date for scheduled activities.
                    scheduledActivity = Activity.objects.get(pk=self.parentActivityId)
                    # if parent activity is schedule for weekly
                    if scheduledActivity.Type == 'Weekly':
                        # update Scheduled Date for tommorrow
                        scheduledActivity.scheduled = self.one_day_hence()
                        scheduledActivity.Description = self.Description
                        scheduledActivity.save()
                        print("Schedule Activity has been rescheduled.")

                   
                
       
            
            
            
       

        


