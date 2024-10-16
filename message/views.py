import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from blog.models import Blog
from message.forms import (
    MessageForm,
    ClientForm,
    MailingListForm,
    MailingListModeratorForm,
    MailingListUpdateForm,
)
from message.models import Message, Client, MailingList
from message.services import (
    get_total_mailings_active_from_cache,
    get_total_items_from_cache,
)


class MessageListView(ListView):
    """
    Контроллер для отображения всех сообщений
    """
    model = Message

    def get_queryset(self):
        """
        Возвращает сообщения текущего пользователя
        """
        if self.request.user.is_superuser:
            return Message.objects.all()
        elif self.request.user.is_authenticated:
            return Message.objects.filter(owner=self.request.user)
        else:
            return Message.objects.none()


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Контроллер для отображения конкретного сообщения
    """
    model = Message

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь просматривать сообщение
        """
        message = self.get_object()
        user = self.request.user
        if user.is_superuser or user == message.owner:
            return True


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Контроллер для создания нового сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("message:message_view")

    def form_valid(self, form):
        """
        Сохраняет сообщение в БД и привязывает его к текущему пользователю
        """
        message = form.save()
        message.owner = self.request.user
        message.save(update_fields=["owner"])
        return super().form_valid(form)

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь создать сообщение
        """
        user = self.request.user
        if user.is_superuser or user.is_authenticated and not user.is_staff:
            return True


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("message:message_view")

    def get_success_url(self):
        return reverse("message:message_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """
        Отображает форму редактирования в зависимости от текущего пользователя
        """
        user = self.request.user
        if self.object.owner == user or user.is_superuser:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер для удаления сообщения
    """
    model = Message
    success_url = reverse_lazy("message:message_view")

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь удалить конкретное сообщение
        """
        message = self.get_object()
        user = self.request.user
        if user.is_superuser or user == message.owner:
            return True


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения всех клиентов
    """
    model = Client

    def get_queryset(self):
        """
        Возвращает клиентов текущего пользователя
        """
        if self.request.user.is_superuser:
            return Client.objects.all()
        if self.request.user.is_authenticated:
            return Client.objects.filter(owner=self.request.user)
        else:
            return Client.objects.none()


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Контроллер для отображения конкретного клиента
    """
    model = Client

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь просматривать конкретного клиента
        """
        client = self.get_object()
        user = self.request.user
        if user.is_superuser or user == client.owner:
            return True


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Контроллер для создания нового клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("message:client_view")

    def form_valid(self, form):
        """
        Сохраняет клиента в БД и привязывает его к текущему пользователю
        """
        client = form.save()
        client.owner = self.request.user
        client.save(update_fields=["owner"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("message:client_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь создавать клиентов
        """
        user = self.request.user
        if user.is_superuser or user.is_authenticated and not user.is_staff:
            return True


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("message:client_view")

    def get_success_url(self):
        return reverse("message:client_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """
        Отображает форму редактирования в зависимости от текущего пользователя
        """
        user = self.request.user
        if self.object.owner == user or user.is_superuser:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер для удаления клиента
    """
    model = Client
    success_url = reverse_lazy("message:client_view")

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь удалять конкретного клиента
        """
        client = self.get_object()
        user = self.request.user
        if user.is_superuser or user == client.owner:
            return True


class MailingListListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения всех рассылок
    """
    model = MailingList

    def get_queryset(self):
        """
        Возвращает рассылки текущего пользователя
        """
        if self.request.user.is_superuser or self.request.user.is_staff:
            return MailingList.objects.all()
        elif self.request.user.is_authenticated:
            return MailingList.objects.filter(owner=self.request.user)


class MailingListCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Контроллер для создания новой рассылки
    """
    model = MailingList
    form_class = MailingListForm

    def get_form_kwargs(self):
        """
        Добавляет исходные данные формы из GET-параметра
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs["initial"]["message"] = self.request.GET.get("id")
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        """
        Обновляет дату следующей отправки при сохранении изменений
        """
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.next_date = mailing.date_and_time_of_sending
        mailing.save(update_fields=["next_date", "owner"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("message:mailinglist_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь создавать рассылки
        """
        user = self.request.user
        if user.is_superuser or user.is_authenticated and not user.is_staff:
            return True


class MailingListDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для отображения конкретной рассылки
    """
    model = MailingList

    def get_context_data(self, **kwargs):
        """
        Добавляет список клиентов к контексту
        """
        context_data = super().get_context_data(**kwargs)
        context_data["clients"] = self.object.clients.all()
        return context_data


class MailingListUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для создания новой рассылки
    """
    model = MailingList
    form_class = MailingListUpdateForm

    def form_valid(self, form):
        """
        Обновляет дату следующей отправки и статус рассылки при сохранении изменений
        """
        mailing = form.save()
        mailing.next_date = mailing.date_and_time_of_sending
        mailing.status = "Запущена"
        mailing.save(update_fields=["next_date", "status"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("message:mailinglist_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """
        Отображает форму удаления в зависимости от текущего пользователя
        """
        user = self.request.user
        if self.object.owner == user or user.is_superuser:
            return MailingListUpdateForm
        elif user.has_perm("message.can_edit_status"):
            return MailingListModeratorForm


class MailingListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер для удаления рассылки
    """
    model = MailingList
    success_url = reverse_lazy("message:mailinglist_view")

    def test_func(self):
        """
        Проверяет, может ли текущий пользователь удалять конкретную рассылку
        """
        user = self.request.user
        mailing = self.get_object()
        if user.is_superuser or user == mailing.owner:
            return True
        return PermissionDenied


@login_required
def toggle_status(request, pk):
    """
    Метод изменения статуса рассылки
    """
    mailing = get_object_or_404(MailingList, pk=pk)
    if mailing.status == "Запущена":
        mailing.status = "Завершена"
    elif mailing.status == "Создана":
        mailing.status = "Запущена"
    mailing.save(
        update_fields=[
            "status",
        ]
    )
    return redirect(reverse("message:mailinglist_view"))


@login_required
def AttemptListView(request, pk):
    """
    Контроллер для отображения всех попыток отправки рассылки
    """
    mailing = get_object_or_404(MailingList, pk=pk)
    attempts = mailing.attempts.all()
    numbers = [number for number in range(1, len(attempts) + 1)]
    context = {"attempts": attempts, "mailing": mailing, "numbers": numbers}
    return render(request, "message/attempt_list.html", context)


def HomePageView(request):
    """
    Контроллер для главной страницы
    """
    template_name = "message/home_page.html"
    total_mailings = get_total_items_from_cache("mailing", MailingList)
    total_active_mailings = get_total_mailings_active_from_cache()
    total_clients = get_total_items_from_cache("clients", Client)
    blogs = get_total_items_from_cache("blogs", Blog)
    blogs_list = []
    for blog in blogs:
        blogs_list.append(blog)
    random.shuffle(blogs_list)

    context = {
        "total_mailings": len(total_mailings),
        "total_active_mailings": len(total_active_mailings),
        "total_clients": len(total_clients),
        "blogs": blogs_list[:3],
    }
    return render(request, template_name, context)