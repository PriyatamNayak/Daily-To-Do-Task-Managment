from django.urls import path
from .views import Home,SettingsLov,SettingsAddLov,SettingsDeleteLov
from .views import TaskList,AddTask,DeleteTask,TaskDetail,TaskUpdate,AddTaskComment,DeleteTaskCommnet,AddLink,TaskCommentList,TaskCommentUpdate
from .views import ActivityDetail,DeleteActivity,ActivityList,AddActivity,ActivityUpdate,CommentsDetail #Activity Related Views
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.login, name ="login"),
    path("logout/", LogoutView.as_view(template_name='projects/login.html'), name="logout"),
    path('Dashboard/', Home.as_view(),name="HomePage"),
    path('setting/lov/', SettingsLov.as_view(),name="lov-view"), #Lov List View
    path('setting/lov/add/', SettingsAddLov.as_view(), name='lov-add'), #Add Lov
    path('setting/lov/<pk>/delete/', SettingsDeleteLov.as_view(), name='lov-delete'), #Delete LOV
    path('task/', TaskList.as_view(),name="task-view"), #Task List View
    path('task/add/', AddTask.as_view(), name='task-add'), #Add Task
    path('task/<pk>/delete/', DeleteTask.as_view(), name='task-delete'), #Delete Task
    path('task/<slug:slug>/', TaskDetail.as_view(),name='task-detail'), 
    path('task/shared/<str:signed_slug>/', views.get_shareable_link,name='shared-task-detail'), 
    path('task/update/<pk>/', TaskUpdate.as_view(), name='task_update'),
    path('task/<pk>/comment/add/', AddTaskComment.as_view(), name='task-comment-add'), #Add Task comment
    path('task/comment/<pk>/delete/', DeleteTaskCommnet.as_view(), name='task-comment-delete'), #Delete Task comment
    path('link/add/', AddLink.as_view(), name='link-add'), #Add Link
    path('activity/add/', AddActivity.as_view(), name='activity-add'), #Add Activity
    path('activity/add/<pk>', AddActivity.as_view(), name='comment-activity-add'), #Add Activity from comment
    path('activity/', ActivityList.as_view(),name="activity-view"), #Activity List View
    path('activity/<slug:slug>', ActivityList.as_view(),name="activity-scheduled"), #Activity List View - scheduled
    path('activity/<pk>/', ActivityDetail.as_view(),name='activity-detail'),  #Detail of Activity
    path('activity/<pk>/delete/', DeleteActivity.as_view(), name='activity-delete'), #Delete Task
    path('activity/update/<pk>/', ActivityUpdate.as_view(), name='activity_update'),
    path('comments/', TaskCommentList.as_view(),name="task-comments-view"), #Task List View & used in tags serach
    path('comments/<slug:slug>/', TaskCommentList.as_view(), name="tagged"), #search on top banner
    path('comments/update/<pk>/', TaskCommentUpdate.as_view(), name='comment_update'),
    path('revision/', CommentsDetail.as_view(), name='revise-comments'), #it shows only one record
    path('revision/<pk>', CommentsDetail.as_view(), name='revise-update-comments'), #it shows only one record
    path('task/<slug:slug>/pdf/', login_required(views.generate_pdf), name='task_as_pdf'),
]