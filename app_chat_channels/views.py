from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import ComposeForm
from .models import Thread, ChatMessage



"""
class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = "thread.html"
    form_class = ComposeForm
    model = ChatMessage

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username = self.kwargs.get("username")
        obj, created = Thread.objects.get_or_create(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path

"""


def thread_view(request, username):
    obj, created = Thread.objects.get_or_create(request.user, username)
    if obj is None:
        raise Http404
    # send obj

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method == "POST":

        form = ComposeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            user = request.user
            chat_message = ChatMessage(user = user, message = message, thread = obj)
            chat_message.save()

    form = ComposeForm()
    context = {
        "object": obj,
        "form": form,
    }

    return render(request, "thread.html", context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created")
            return redirect('login')

    else:
        form = UserCreationForm()
        context = {
            'form': form,
        }

    return render(request, "signup.html", context)

