from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from task_manager.statuses.models import Statuses
from task_manager.statuses.forms import StatusForm
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequired
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext
from django.contrib import messages

# Create your views here.


class StatusesListView(AuthRequired, ListView):
    template_name = "statuses/list.html"
    model = Statuses


class StatusesCreateView(AuthRequired, SuccessMessageMixin, CreateView):
    template_name = "statuses/create.html"
    model = Statuses
    form_class = StatusForm
    success_url = reverse_lazy("statuses:list")
    success_message = gettext("Status create")


class StatusesUpdateView(AuthRequired, SuccessMessageMixin, UpdateView):
    template_name = "statuses/update.html"
    model = Statuses
    form_class = StatusForm
    success_url = reverse_lazy("statuses:list")
    success_message = gettext("Status update")


class StatusesDeleteView(AuthRequired, SuccessMessageMixin, DeleteView):
    template_name = "statuses/delete.html"
    model = Statuses
    success_url = reverse_lazy("statuses:list")
    success_message = gettext("Status delete")

    def post(self, request, *args, **kwargs):
        if self.get_object().status.all().exists():
            messages.error(self.request, gettext("status to delete unreal"))
            return redirect("statuses:list")
        return super().post(request, *args, **kwargs)
