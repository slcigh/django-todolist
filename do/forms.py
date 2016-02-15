from django import forms
from do.models import Project, Task
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' add project here...'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProjectForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        name = cleaned_data.get('name')
        project_list = Project.objects.filter(create_by=self.request.user)
        for project in project_list:
            if project.name == name:
                raise forms.ValidationError('project name already exists.')

    class Meta:
        model = Project
        exclude = ['create_by']


class TaskForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' add task here...'}))
    target_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': ' click to select target date... '}))

    class Meta:
        model = Task
        exclude = ['project']
        fields = ('content', 'target_date')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
