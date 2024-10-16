from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, TextInput, DateTimeField

from message.models import Message, Client, MailingList


class StyleFormMixin:
    """
    Mixin для стилизации формы.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field, DateTimeField):
                field.widget.attrs["class"] = "form-datetime-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageForm(StyleFormMixin, ModelForm):
    """
    Форма для создания нового сообщения
    """
    class Meta:
        model = Message
        fields = ("title_letter", "body_letter")
        widgets = {
            "title_letter": TextInput(attrs={"placeholder": "Введите тему сообщения"}),
        }


class ClientForm(StyleFormMixin, ModelForm):
    """
    Форма для создания нового клиента
    """
    class Meta:
        model = Client
        fields = ("name", "email", "comment")
        widgets = {
            "name": TextInput(attrs={"placeholder": "Введите Ф.И.О."}),
            "email": TextInput(attrs={"placeholder": "Введите Email"}),
            "comment": TextInput(attrs={"placeholder": "Введите текст"}),
        }


class MailingListForm(StyleFormMixin, ModelForm):
    """
    Форма для создания и изменения рассылки сообщения
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(MailingListForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["clients"].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = MailingList
        fields = (
            "message",
            "clients",
            "date_and_time_of_sending",
            "periodicity",
        )

    def clean_message(self):
        """
        Проверяет наличие уже имеющейся рассылки с таким сообщением
        """
        new_message = self.cleaned_data["message"]
        if MailingList.objects.filter(message=new_message.pk).exists():
            raise ValidationError("Рассылка с этим сообщением уже имеется")
        return new_message

    def clean_date_and_time_of_sending(self):
        """
        Проверяет, что дата и время рассылки не меньше текущего.
        """
        date_and_time = self.cleaned_data["date_and_time_of_sending"]
        if date_and_time.timestamp() < datetime.now().timestamp():
            raise ValidationError("Выбранная дата и время меньше текущего")
        return date_and_time


class MailingListUpdateForm(StyleFormMixin, ModelForm):
    """
    Форма для изменения рассылки сообщения
    """
    class Meta:
        model = MailingList
        fields = (
            "message",
            "clients",
            "date_and_time_of_sending",
            "periodicity",
        )

    def clean_date_and_time_of_sending(self):
        """
        Проверяет, что дата и время рассылки не меньше текущего.
        """
        date_and_time = self.cleaned_data["date_and_time_of_sending"]
        if date_and_time.timestamp() < datetime.now().timestamp():
            raise ValidationError("Выбранная дата и время меньше текущего")
        return date_and_time


class MailingListModeratorForm(StyleFormMixin, ModelForm):
    """
    Форма для создания рассылки сообщения
    """
    class Meta:
        model = MailingList
        fields = ("status",)