from healthy_life_site.settings import AUTH_USER_MODEL
from django.db import models


class StatusMessage(models.IntegerChoices):
    DISPLAYED = 0, 'Отображается'
    DELETED = 1, 'Удалено'


class Notifications(models.Model):
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    user_notify = models.OneToOneField(AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='user_notify_fk',
                                       verbose_name='Уведомляемый пользователь')
    message = models.CharField(max_length=1024, verbose_name='Сообщение')
    date_notify = models.DateTimeField(auto_now_add=True, verbose_name='Время события')

    objects = models.Manager()


class IMessage(models.Model):
    class Meta:
        abstract = True
        ordering = ['date_create']

    reply = models.ForeignKey('self', on_delete=models.PROTECT, null=True,
                              related_name='%(app_label)s_%(class)s_reply', verbose_name='Ответ на сообщение')
    wrote = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,
                              related_name='%(app_label)s_%(class)s_wrote', verbose_name='Написал')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время написания')
    date_change = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    message = models.TextField(max_length=4_096, verbose_name='Сообщение')
    status = models.PositiveSmallIntegerField(choices=StatusMessage.choices, default=StatusMessage.DISPLAYED,
                                              verbose_name='Статус')

    class DisplayedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=StatusMessage.DISPLAYED)

    objects = models.Manager()
    displayed = DisplayedManager()

