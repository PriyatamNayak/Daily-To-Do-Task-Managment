from django.contrib import admin
from .models import ApplictaionData,ProjectTask,TaskComment,FavLink,Activity

# Register your models here.
admin.site.register(ApplictaionData)
admin.site.register(ProjectTask)
admin.site.register(TaskComment)
admin.site.register(FavLink)
admin.site.register(Activity)