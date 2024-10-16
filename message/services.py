from datetime import datetime, timedelta
from smtplib import SMTPException

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config.settings import EMAIL_HOST_USER
from message.models import MailingList, Attempt, Client


def sending_a_message(item: MailingList):
    """
    Отправка сообщения клиенту с использованием SMTP
    """
    try:
        send_mail(
            item.message.title_letter,
            item.message.body_letter,
            EMAIL_HOST_USER,
            [x.email for x in item.clients.all()],
            fail_silently=False,
        )
    except SMTPException as message:
        Attempt.objects.create(mailing_list=item, mail_server_response=f"{message}")
    else:
        Attempt.objects.create(
            mailing_list=item, status="Успешно", mail_server_response="Доставлено"
        )


def periodicity_sending():
    """
    Отправка сообщения клиенту каждый день
    """
    mailing_list = MailingList.objects.filter(next_date__lte=datetime.now())
    for mailing in mailing_list:
        if mailing.status == "Запущена":
            sending_a_message(mailing)
            if mailing.periodicity == "Раз в день":
                mailing.next_date = mailing.next_date + timedelta(days=1)
            if mailing.periodicity == "Раз в неделю":
                mailing.next_date = mailing.next_date + timedelta(days=7)
            if mailing.periodicity == "Раз в месяц":
                mailing.next_date = mailing.next_date + timedelta(days=30)
            mailing.save(update_fields=["next_date"])


def get_total_items_from_cache(key_name: str, model_name):
    """
    Получение всех записей из кеша, если в кеше нет, то получение через БД
    """
    if settings.CACHE_ENABLED:
        key = key_name
        item_list = cache.get(key)
        if item_list is None:
            item_list = model_name.objects.all()
            cache.set(key, item_list)
    else:
        item_list = model_name.objects.all()

    return item_list


def get_total_mailings_active_from_cache():
    """
    Получение всех активных рассылок, если в кеше нет, то получение через БД
    """
    if settings.CACHE_ENABLED:
        key = "mailing_active"
        mailing_active_list = cache.get(key)
        if mailing_active_list is None:
            mailing_active_list = MailingList.objects.filter(status="Запущена")
            cache.set(key, mailing_active_list)
    else:
        mailing_active_list = MailingList.objects.filter(status="Запущена")

    return mailing_active_list