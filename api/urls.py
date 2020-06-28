from rest_framework import routers
from .api import ActivityListGeneric,ActivityCreate,ActivityDetailGeneric
from .views import ActivityList,ActivityDetail,ScheduledActivityList,ActivityDone
from .views import RevisionItem,RevisionItemUpdate
from .views import RevisionItemofTheDay,all_task,all_task_items
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path
urlpatterns = [
path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
path("api/activities/scheduled", ScheduledActivityList.as_view(), name="activity_api_list"), # in-use for activity creation
path("api/activities/done/<int:pk>/", ActivityDone.as_view(), name="activity_api_list"), # in-use for making activity done
path("api/revision/", RevisionItem.as_view(), name="revision_item"), # in-use for making activity done
path("api/revision/<int:pk>/", RevisionItemUpdate.as_view(), name="revision_item_update"), # update updated field
path("api/dailytask/", RevisionItemofTheDay.as_view(), name="daily_task"), # daily_task
path("api/task/comments/<int:pk>/", all_task_items.as_view(), name="all_task_items"), # all_commnet_on_specific_task

]

# router has been used in activity creation API.
from rest_framework.routers import DefaultRouter
from .apiview import ActivityViewSet,TaskCommentViewSet,TaskViewSet

router = DefaultRouter()
router.register('ActivityRouter', ActivityViewSet,'api-activity')  #create activity
router.register('TaskCommentRouter', TaskCommentViewSet,'api-task-coment')  #create taskcomment
router.register('TaskRouter', TaskViewSet,'api-task')  #create Task

urlpatterns += router.urls
