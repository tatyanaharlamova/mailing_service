from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.models import Client


def index(request):
    """
    Контроллер главной страницы
    """
    return render(request, 'mailing/index.html')


class ClientListView(ListView):
    """
    Контроллер отвечающий за отображение списка клиентов
    """
    model = Client


class ClientDetailView(DetailView):
    """
    Контроллер отвечающий за отображение клиента
    """
    model = Client


class ClientCreateView(CreateView):
    """
    Контроллер отвечающий за создание клиента
    """
    model = Client
    fields = ['name', 'email', 'comment']
    success_url = reverse_lazy('mailing:clients_list')


class ClientUpdateView(UpdateView):
    """
    Контроллер отвечающий за редактирование клиента
    """
    model = Client
    fields = ['name', 'email', 'comment']
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(DeleteView):
    """
    Контроллер отвечающий за удаление клиента
    """
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


