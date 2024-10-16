import secrets

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm, UserModeratorForm
from users.models import User


class UserRegisterView(CreateView):
    """
    Форма создания нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            "Подтверждение почты",
            f"Перейдите по ссылке для подтверждения почты: {url}",
            EMAIL_HOST_USER,
            [user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Перевод пользователя в статуc Активный при проходе по ссылке с почты
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Вывод информации о пользователе
    """
    model = User


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Вывод списка всех пользователей
    """
    model = User
    permission_required = ("users.view_user",)

    def get_queryset(self):
        """
        Возвращает всех пользователей, кроме суперпользователя
        """
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            queryset = queryset.exclude(is_superuser=True)
        elif self.request.user.is_staff:
            queryset = queryset.exclude(is_staff=True)
        return queryset


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("message:message_list")

    def get_success_url(self):
        return reverse("users:user_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """
        Отображает форму редактирования в зависимости от пользователя
        """
        profile = self.request.user
        if profile.is_superuser or profile == self.object:
            return UserUpdateForm
        if profile.has_perm("users.can_edit_is_active"):
            return UserModeratorForm
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Вывод формы удаления пользователя
    """
    model = User
    success_url = reverse_lazy("users:user_view")

    def test_func(self):
        """
        Проверка пользователя на принадлежность к суперпользователю
        """
        return self.request.user.is_superuser


@login_required
@permission_required("users.can_edit_is_active")
def toggle_is_active(request, pk):
    """
    Включает/выключает активность пользователя
    """
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    elif not user.is_active:
        user.is_active = True
    user.save(update_fields=["is_active"])
    return redirect(reverse("users:user_view"))