from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from uuslug import slugify


class ProjectManager(models.Manager):
    def create_project(self, name, create_by):
        project = self.create(name=name, create_by=create_by)
        return project


class Project(models.Model):
    create_by = models.ForeignKey(User)
    name = models.TextField()
    slug = models.SlugField(max_length=60, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    objects = ProjectManager()

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project)
    content = models.TextField(max_length=256)
    create_date = models.DateField(auto_now=True)
    target_date = models.DateField(blank=True, null=True)
    finished_date = models.DateField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.is_finished:
            self.finished_date = datetime.now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['target_date']
