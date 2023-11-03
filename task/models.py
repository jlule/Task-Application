from django.db import models
from django.contrib.auth.models import User
#this where you create the databse structure
#user model takes care of user model like email password
#Create your models here.
#creating a one to many relationship

class Task(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True) #models.CASCADe means that if a user gets deleted then the child tasks are deleted aswell. To keep the tasks if user is deleted is models.SET

    title = models.CharField(max_length = 200)
    
    description = models.TextField(null=True, blank=True)

    complete = models.BooleanField(default=False)

    create = models.DateTimeField(auto_now_add=True)

    # string representation of the model
    def __str__(self): 
        return self.title

    #any complete task should be displayed and ordered by the term 'ordered'
    class Meta:
        ordering = ['complete']
 #once complete run command python manage.py makemigrations 
 #and then python manage.py migrate
 #for us to see the model in the admin panel we have to register it in
 #in the admin.py