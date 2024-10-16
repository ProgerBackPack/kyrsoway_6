from django.urls import path

from message.apps import MessageConfig
from message.views import (
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MailingListListView,
    MailingListDetailView,
    MailingListCreateView,
    MailingListUpdateView,
    MailingListDeleteView,
    toggle_status,
    AttemptListView,
    HomePageView,
)

app_name = MessageConfig.name

urlpatterns = [
    path("", HomePageView, name="home_page_view"),
    path("messages/", MessageListView.as_view(), name="message_view"),
    path("message/<int:pk>", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/<int:pk>/delete-confirm/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("clients/", ClientListView.as_view(), name="client_view"),
    path("clients/<int:pk>", ClientDetailView.as_view(), name="client_detail"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path(
        "clients/<int:pk>/delete-confirm/",
        ClientDeleteView.as_view(),
        name="client_delete",
    ),
    path("mailing-list/", MailingListListView.as_view(), name="mailinglist_view"),
    path(
        "mailing-list/<int:pk>",
        MailingListDetailView.as_view(),
        name="mailinglist_detail",
    ),
    path(
        "mailing-list/create/",
        MailingListCreateView.as_view(),
        name="mailinglist_create",
    ),
    path(
        "mailing-list/<int:pk>/update/",
        MailingListUpdateView.as_view(),
        name="mailinglist_update",
    ),
    path(
        "mailing-list/<int:pk>/delete/",
        MailingListDeleteView.as_view(),
        name="mailinglist_delete",
    ),
    path("mailing-list/<int:pk>/activate/", toggle_status, name="toggle_status"),
    path("mailing-list/<int:pk>/attempt/", AttemptListView, name="attempt_list"),
]