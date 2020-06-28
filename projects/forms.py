from django.forms import ModelForm
from .models import ApplictaionData, ProjectTask,TaskComment,FavLink,Activity # models
from django import forms 
from tinymce.widgets import TinyMCE
from taggit.forms import *
from django.utils import timezone



class LovCreateForm(forms.ModelForm):
    '''
    Drop Down value creation form
    '''
    Name = forms.CharField(label='Name',required=False,label_suffix="",widget = forms.TextInput(attrs={'class':'form-control'}))
    Value = forms.CharField(label='Value',required=False,label_suffix="",widget = forms.TextInput(attrs={'class':'form-control'})) 
    Description = forms.CharField(label='Description',required=False,label_suffix="",widget = forms.TextInput(attrs={'class':'form-control'})) 
    IsCategory = forms.BooleanField(label='Is Category',label_suffix="",widget=forms.CheckboxInput(), required=False) 
    Type = forms.ModelChoiceField(label='Type',required=False,queryset=ApplictaionData.objects.filter(IsCategory=True),label_suffix="",widget= forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = ApplictaionData
        fields = ['Name','Value','Description','IsCategory','Type']
    
    #Validation for name Field
    def clean_Description(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("Description") == "":                         
                    raise forms.ValidationError("Description should not be blank.")
        return cleaned_data['Description']

    def clean_Name(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("Name") == "":                         
                    raise forms.ValidationError("Name should not be blank.")
        return cleaned_data['Name']

    def clean_IsCategory(self):
            cleaned_data = self.cleaned_data
            if cleaned_data.get("IsCategory"):
                if cleaned_data.get("Value") != '':                            
                            raise forms.ValidationError("Value should be blank if isCategory is True.")
                elif  cleaned_data.get("Type") != None:                            
                            raise forms.ValidationError("Type should be blank if isCategory is True.")
                elif  cleaned_data.get("Description") == '':
                            raise forms.ValidationError("Description should not be blank if isCategory is True.")
            else:
               
                if  cleaned_data.get("Description") == '':
                            raise forms.ValidationError("Description should not be blank.")
            return cleaned_data['IsCategory']


class ProjectTaskCreateForm(forms.ModelForm):
    '''
    Task creation form - Like working on some major task
    '''
    Task_Title = forms.CharField(label='Title',required=False,label_suffix="",widget = forms.TextInput(attrs={'class':'form-control'})) 
    Task_Description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20,'class':'form-control'}))

    class Meta:
        model = ProjectTask
        fields = ['Task_Description','Task_Title']
    
    #Validation for name Field
    def clean_Description(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("Description") == "":                         
                    raise forms.ValidationError("Description should not be blank.")
        return cleaned_data['Description']

class ProjectTaskCommentCreateForm(forms.ModelForm):
    '''
    Task comment creation form
    '''
    required_css_class = 'required'
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 10,'class': 'form-control'}))
    task = forms.ModelChoiceField(queryset=ProjectTask.objects.all(), empty_label="Select Task", widget=forms.Select(attrs={'class': 'form-control'}))
    tags = TagField() 
    class Meta:
        model = TaskComment
        fields = ['content','task','tags']
    
    def __init__(self, *args, **kwargs):
        taskid = kwargs.pop('taskid', None)
        super().__init__(*args, **kwargs)
        if taskid != None:
            self.fields['task'].queryset = self.fields['task'].queryset.filter(pk=taskid)

class LinkCreateForm(forms.ModelForm):
    '''
    Link creation form
    '''
    link = forms.URLField(label='link',required=True,label_suffix="",widget = forms.TextInput(attrs={'class':'form-control'})) 
    name = forms.CharField(label='name',required=True,label_suffix="",widget = forms.TextInput(attrs={'class':'form-control'})) 
    
    class Meta:
        model = FavLink
        fields = ['name','link',]

class ActivityCreateForm(forms.ModelForm):
    '''
    Activity creation form
    '''
    required_css_class = 'required'
    Description = forms.CharField(
                            label='detail',
                            required=True,
                            label_suffix="",
                            widget=TinyMCE(attrs={'cols': 100, 'rows': 10,'class': 'form-control'})
                            ) 
    Title = forms.CharField(
                            label='Title',
                            required=True,
                            label_suffix="",
                            widget = forms.TextInput(attrs={'class':'form-control'})
                            ) 
    status =forms.ModelChoiceField(
                                    to_field_name="Name", #DataBase not storing Id but storing name
                                    label_suffix="",
                                    required=True,
                                    empty_label='---------',
                                    queryset=ApplictaionData.objects.filter(Type__Name__contains='Activity_Status'),                                    
                                    widget = forms.Select(attrs={'class':'form-control'})
                                    )
    Type =forms.ModelChoiceField(
                                    
                                    to_field_name="Name", #DataBase not storing Id but storing name
                                    label_suffix="",
                                    empty_label='---------',
                                    required=True,
                                    queryset=ApplictaionData.objects.filter(Type__Name__contains='Activity_Type'), 
                                    widget = forms.Select(attrs={'class':'form-control'})
                                )
    scheduled=forms.DateField(
                                label_suffix="",
                                required=False,
                                widget = forms.SelectDateWidget(years=['2020','2021','2022'], 
                                empty_label=("Choose Year", "Choose Month", "Choose Day"),)
                            )
    class Meta:
        model = Activity
        fields = ['Title','Description','status','scheduled','Type']
        
    def __init__(self, *args, **kwargs):
        print('activity_create_Form __init__')
        commentId = kwargs.pop('commentId', None)
        super().__init__(*args, **kwargs)
        print(self.fields)
        if commentId is not None:
            print("Activity is Created from comment.",commentId)
            comment = TaskComment.objects.get(pk=commentId)           
            self.fields['Description'].initial  = comment.content

    def clean_scheduled(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data.get("scheduled"))
        if cleaned_data.get("scheduled") is None:                         
                    raise forms.ValidationError("scheduled should not be blank.")
        return cleaned_data['scheduled']
    
    def clean_Type(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data.get("Type"))
        if cleaned_data.get("Type") is None:                         
                    raise forms.ValidationError("Type should not be blank.")
        return cleaned_data['Type']
            
        
       
       

