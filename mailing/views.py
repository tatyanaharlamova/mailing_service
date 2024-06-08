from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, Log
from mailing.services import send_mailing


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
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')

    def form_valid(self, form):
        obj = form.save()
        send_mailing(obj)
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """
    Контроллер отвечающий за редактирование клиента
    """
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:view', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    """
    Контроллер отвечающий за удаление клиента
    """
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


class MessageListView(ListView):
    """
    Контроллер отвечающий за отображение списка сообщений
    """
    model = Message


class MessageDetailView(DetailView):
    """
    Контроллер отвечающий за отображение сообщения
    """
    model = Message


class MessageCreateView(CreateView):
    """
    Контроллер отвечающий за создание сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages_list')


class MessageUpdateView(UpdateView):
    """
    Контроллер отвечающий за редактирование сообщение
    """
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:view_message', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    """
    Контроллер отвечающий за удаление сообщения
    """
    model = Message
    success_url = reverse_lazy('mailing:messages_list')


class MailingListView(ListView):
    """
    Контроллер отвечающий за отображение списка рассылок
    """
    model = Mailing


class MailingDetailView(DetailView):
    """
    Контроллер отвечающий за отображение рассылки
    """
    model = Mailing


class MailingCreateView(CreateView):
    """
    Контроллер отвечающий за создание рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings_list')


class MailingUpdateView(UpdateView):
    """
    Контроллер отвечающий за редактирование рассылки
    """
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:view_mailing', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    """
    Контроллер отвечающий за удаление расылки
    """
    model = Mailing
    success_url = reverse_lazy('mailing:mailings_list')


class LogListView(ListView):
    """
    Контроллер отвечающий за отображение списка логов
    """
    model = Log
