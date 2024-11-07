from healthy_life_site.settings import AUTH_USER_MODEL
from common.models import IMessage
from pharmacy.models import Goods
from django.db import models


class ActionLog(models.IntegerChoices):
    BAN = 0, 'Блокировки'
    ROLE = 1, 'Роли'
    GOODS = 2, 'Товары'
    BLOG = 3, 'Блоги'
    REMOVE_USER = 4, 'Удаление пользователя'


class SatusOrder(models.IntegerChoices):
    IN_DELIVERY = 0, 'Доставляется'
    DELIVERED = 1, 'Доставлено'
    CANCELLED = 2, 'Отменено'


class BanCommunication(models.Model):
    class Meta:
        verbose_name = 'Блокировка общения'
        verbose_name_plural = 'Блокировки общения'

    who_banned = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name='who_banned_fk', verbose_name='Кто забанил')
    got_banned = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name='got_banned_fk', verbose_name='Забаненный')
    banned_date = models.DateTimeField(auto_now_add=True, verbose_name='Когда забанели')

    ban_time = models.DurationField(null=True, verbose_name='Время бана')

    objects = models.Manager()


class AdminLog(models.Model):
    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    time_log = models.DateTimeField(auto_now_add=True, verbose_name='Когда было совершено')
    code_log = models.PositiveSmallIntegerField(choices=ActionLog.choices, verbose_name='Код лога')
    log_info = models.CharField(max_length=1024, verbose_name='Информация')

    objects = models.Manager()


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    goods_order = models.ForeignKey(Goods,
                                    on_delete=models.PROTECT,
                                    related_name='goods_order_fk',
                                    verbose_name='Товар заказа')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_complete = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    status_order = models.PositiveSmallIntegerField(choices=SatusOrder, default=SatusOrder.IN_DELIVERY,
                                                    verbose_name='Статус заказа')

    objects = models.Manager()


class OrderMessage(IMessage):
    class Meta:
        verbose_name = 'Сообщение заказа'
        verbose_name_plural = 'Сообщения заказов'

    order = models.ForeignKey(Order,
                              on_delete=models.PROTECT,
                              related_name='order_fk',
                              verbose_name='Заказ')
