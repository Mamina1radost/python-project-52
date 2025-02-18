from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from task_manager.users.forms import Create, Update
from task_manager.mixins import AuthRequired
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


class UsersListView(ListView):
    template_name = 'users/list.html'
    model = get_user_model()
    


class UsersCreate(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = 'users/create.html'
    form_class = Create
    success_url = reverse_lazy('login')
    success_message = gettext('User register successfull')

class UsersUpdate(AuthRequired, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = Update
    template_name = 'users/update.html'
    success_url = '/users/'
    success_message = gettext('User update successfull')


class UsersDelete(AuthRequired, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = '/users/'
    success_message = gettext('User delete successfull')


