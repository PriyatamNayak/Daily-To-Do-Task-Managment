from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView,CreateView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import ApplictaionData,ProjectTask,TaskComment,FavLink,Activity  #import models
from django.conf import settings
from .forms import LovCreateForm, ProjectTaskCreateForm,ProjectTaskCommentCreateForm,LinkCreateForm,ActivityCreateForm #import forms
from django.urls import reverse_lazy
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import datetime ,timedelta
from django.contrib import messages
from django.core.signing import BadSignature
#pdf generate
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.http import  HttpResponse


def login(request):
    if request.method =="POST":
        username = request.POST['username']
        password =request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            return redirect("Dashboard/")
        else :            
            messages.error(request, f"Invalid credential!")           
            return redirect('login')
        pass
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('HomePage'))
        else:
          return render(request,"projects/login.html")

class Home(LoginRequiredMixin,FormView):
    '''
    home page as templateview with context
    change from templateview to FormView
    '''
    form_class = ProjectTaskCommentCreateForm
    template_name = 'projects/index.html' 
    success_url = reverse_lazy('HomePage')

    def form_valid(self, form):
        notes = form.save(commit=False)
        notes.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        return super().form_valid(form) 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['links'] = FavLink.objects.all()
        revision_data=[]
        revision_label=[]
        revision_queryset = TaskComment.objects.all().annotate(updated_date=TruncDate('updated')).order_by('-updated_date').values('updated_date').annotate(**{'total': Count('updated')})[0:5]
        for r in revision_queryset:
            revision_data.append(r["total"])
            revision_label.append(r["updated_date"].strftime("%Y-%m-%d"))            
        context['revision_label'] = revision_label
        context['revision_data'] = revision_data
        if len(revision_data)>0 :
            context['revision_width'] = revision_data[0] * 2 
        else :
              context['revision_width'] = 0
        activity_data=[]
        actiivity_label=[]
        activity_queryset = Activity.objects.filter(status="Done").annotate(updated_date=TruncDate('updated')).order_by('-updated_date').values('updated_date').annotate(**{'total': Count('updated')})[0:5]
        for r in activity_queryset:
            activity_data.append(r["total"])
            actiivity_label.append(r["updated_date"].strftime("%Y-%m-%d"))            
        context['activity_data'] = activity_data
        if len(activity_data)>0 :
               context['activity_width'] = activity_data[0] * 10
        else:
             context['activity_width'] =0
        context['activity_label'] = actiivity_label
        context['activity_form'] = ActivityCreateForm()
        dt = datetime.now()
        context['tasks']= queryset = Activity.objects.filter(scheduled__lte=dt,Type='General').exclude(status='Done').order_by('scheduled')[0:5]
        
        return context

class SettingsLov(LoginRequiredMixin,ListView):
    '''
    List view of drop down values
    all drop down values will be maintained in Applictaion data
    '''
    template_name ='projects/list_of_value.html'
    paginate_by = settings.NUM_OF_RECORD_IN_LIST_VIEW
    model = ApplictaionData
    context_object_name ='records'

class SettingsAddLov(LoginRequiredMixin,CreateView):
        '''
        Add drop down value
        '''
        template_name ='projects/add_list_of_value.html'
        model = ApplictaionData
        form_class=LovCreateForm

class SettingsDeleteLov(LoginRequiredMixin,DeleteView):
        '''
        delete drop down value
        '''
        model = ApplictaionData
        success_url =reverse_lazy('lov-view')

class TaskList(LoginRequiredMixin,ListView):
    '''
    List view of Tasks
    '''
    template_name ='projects/list_of_tasks.html'
    paginate_by = settings.NUM_OF_RECORD_IN_LIST_VIEW
    context_object_name ='records'
    def get_queryset(self):
          queryset = ProjectTask.objects.all().order_by("-pk")
          return queryset

class AddTask(LoginRequiredMixin,CreateView):
        '''
        Add task
        '''
        template_name ='projects/add_task.html'
        model = ProjectTask
        form_class=ProjectTaskCreateForm

class DeleteTask(LoginRequiredMixin,DeleteView):
        '''
        delete task
        '''
        model = ProjectTask
        success_url =reverse_lazy('task-view')

class TaskDetail(LoginRequiredMixin,DetailView):
    '''
    detail of task
    '''
    model = ProjectTask 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = TaskComment.objects.filter(task__slug=self.kwargs.get("slug")).order_by('-pk')
        absolute_url = self.request.build_absolute_uri(ProjectTask.objects.get(slug=self.kwargs.get("slug")).get_absolute_url())
        context['absolute_url'] =absolute_url

        return context

def get_shareable_link(request, signed_slug):
    '''
    Sharable link
    '''
    try:
        slug = ProjectTask.signer.unsign(signed_slug)
        task = ProjectTask.objects.get(slug=slug)
        absolute_url = request.build_absolute_uri(ProjectTask.objects.get(slug=slug).get_absolute_url())       
        context = {
            'comments': TaskComment.objects.filter(task__slug=slug).order_by('-pk'),
            'absolute_url':absolute_url,
            'projecttask':task
        }
        return render(request, 'projects/projecttask_detail.html', context)
    except (BadSignature, ProjectTask.DoesNotExist):
        raise Http404('No Order matches the given query.')
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def render_to_pdf(template_src, context_dict={}):
    '''
        generate pdf from html
    '''
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result,link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error Rendering PDF", status=400)
    

def generate_pdf(request, slug):
    '''
    generate pdf
    '''
    task = get_object_or_404(ProjectTask, slug=slug)
    absolute_url = request.build_absolute_uri(task.get_absolute_url())   
    context = {
            'comments': TaskComment.objects.filter(task__slug=slug).order_by('-pk'),
            'absolute_url':absolute_url,
            'projecttask':task,
            'pagesize':'A4',
    }
    pdf = render_to_pdf('projects/task_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "{}.pdf".format(task.slug)
        content = "inline; filename={}".format(filename)
        content = "attachment; filename={}".format(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
         
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = ProjectTask
    fields = ['Task_Description']
    template_name_suffix = '_update_form'

    def get_success_url(self, **kwargs):
        next = self.request.POST.get('next', '/')
        return next
    

class AddTaskComment(LoginRequiredMixin,CreateView):
        '''
        Add task
        '''
        template_name ='projects/add_task_comment.html'
        model = TaskComment
        form_class=ProjectTaskCommentCreateForm
        def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['taskid'] = self.kwargs.get("pk")
            return kwargs
        
        def get_success_url(self, **kwargs):
            #next page implementation after form submit
            next = self.request.POST.get('next', '/')
            return next
            
class DeleteTaskCommnet(LoginRequiredMixin,DeleteView):
        '''
        delete task
        '''
        model = TaskComment
        def get_success_url(self):
            return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})
        
        
class AddLink(LoginRequiredMixin,CreateView):
        '''
        Add favourite link
        '''
        template_name ='projects/add_link.html'
        model = FavLink
        form_class=LinkCreateForm
        success_url =reverse_lazy('HomePage')

class AddActivity(LoginRequiredMixin,CreateView):
        '''
        Add favourite link
        '''
        template_name ='projects/add_activity.html'
        model = Activity
        form_class=ActivityCreateForm
        success_url =reverse_lazy('activity-view')
        def get_form_kwargs(self):
            '''
            if converting activity from comment
            '''
            kwargs = super().get_form_kwargs()
            kwargs['commentId'] = self.kwargs.get("pk",None)
            return kwargs

class ActivityList(LoginRequiredMixin,ListView):
    '''
    List view of Activities
    Old activities should list first
    list scheduled activities
    once Weekly Activity is done, only Weekly scheduled activity will be rescheduled for next date  
    Yearly and monthly activities will be required to reschedule manually.  
    '''
    template_name ='projects/list_of_activities.html'
    paginate_by = settings.NUM_OF_RECORD_IN_LIST_VIEW
    model = Activity
    context_object_name ='records'
    def get_queryset(self):
        if self.kwargs.get("slug",None) == "scheduled": #search for scheduled activity           
            queryset = Activity.objects.exclude(Type='General').order_by('scheduled')   
        elif self.kwargs.get("slug",None) == "all": #search for all activity
            queryset = Activity.objects.all().order_by('-scheduled')      
        else:
            dt = datetime.now()
            # Order by is important to display old activity first and newly created activity later
            queryset = Activity.objects.filter(scheduled__lte=dt,Type='General').exclude(status='Done').order_by('scheduled')            
        return queryset

class ActivityDetail(LoginRequiredMixin,DetailView):
    '''
    detail of Activity
    '''
    model = Activity 
    success_url =reverse_lazy('activity-list')

class DeleteActivity(LoginRequiredMixin,DeleteView):
        '''
        delete Activity
        '''
        model = Activity
        success_url =reverse_lazy('activity-view')

class ActivityUpdate(LoginRequiredMixin,UpdateView):
    model = Activity
    form_class=ActivityCreateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        '''
        to generate next page after submit
        '''
        next = self.request.POST.get('next', '/')
        return next

    def get_form_kwargs(self):
            '''
            it will be used in form init, we can pass variable from here to form init
            '''
            print('View method : ActivityUpdate, get_form_kwargs')
            kwargs = super().get_form_kwargs()
            return kwargs

class TaskCommentList(LoginRequiredMixin,ListView):
    '''
    List view of Tasks - Revision
    Search based on Tag
    '''
    template_name ='projects/list_of_taskcomments.html'
    paginate_by = settings.NUM_OF_RECORD_IN_LIST_VIEW
    context_object_name ='records'
    def get_queryset(self):
        queryset = TaskComment.objects.all()
        if self.kwargs.get("slug",None): #search based on tags
            slug = self.kwargs.get("slug",None)            
            queryset = TaskComment.objects.filter(tags__name__in=[slug,])
        else:
            queryset = TaskComment.objects.all().order_by('-pk')            
        return queryset

class TaskCommentUpdate(LoginRequiredMixin,UpdateView):
    model = TaskComment
    # form_class=ProjectTaskCommentCreateForm
    template_name_suffix = '_update_form'
    fields = ['content', 'tags', ]

class CommentsDetail(LoginRequiredMixin,ListView):
    '''
    revision section
    '''
    template_name ='projects/list_of_taskcomments.html'
    context_object_name ='records'
    def get_queryset(self):
        queryset = TaskComment.objects.all().order_by('-created')
        if self.kwargs.get("pk",None): #search based on tags
            queryset = TaskComment.objects.all().order_by('updated')
            pk =  self.kwargs.get("pk",None)
            comment = TaskComment.objects.get(pk=pk)
            comment.updated=timezone.now()
            comment.save()
        return queryset[:1]






        
    


       
