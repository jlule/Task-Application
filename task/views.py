#view is the html page 
# that is displayed in the browser
#project.urls that requests  url from apps.urls which gets views from views.urls
from django.shortcuts import render, redirect


from django.views.generic.list import ListView

from django.views.generic.detail import DetailView

#looks for view ending in  _detail.html
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
#looks for view ending in _form.html
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



from .models import Task

#views is what is to be  displayed
#class use the model so you have to import the model you created


class CustomLoginView(LoginView):
    template_name = 'task/login.html'
    fields ='__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'task/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
   model = Task
   context_object_name = 'tasks'


def get_context_data(self, **kwargs):

       context = super().get_context_data(**kwargs)

       context['tasks'] = context['tasks']. filter(user = self.request.user)

       context['count'] = context['tasks']. filter(complete = False).count()

       search_input = self.request.GET.get('search-area') or ''
       
       if search_input:
           context['tasks'] = context['tasks'].filter(
               title__startswith = search_input)
       context['search_input'] = search_input
       


       return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name ='task'
    template_name ='task/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


    def form_invalid(Self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields ='__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
