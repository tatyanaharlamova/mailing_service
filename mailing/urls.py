from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import index, ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView, ClientDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('clients_list/', ClientListView.as_view(), name='clients_list'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='view'),
]
