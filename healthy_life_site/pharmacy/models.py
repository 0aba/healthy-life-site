from healthy_life_site.settings import AUTH_USER_MODEL
from common.models import IMessage
from django.db import models


class TypeGoods(models.IntegerChoices):
    OTHER = 0, 'Другое'
    MEDICINE = 1, 'Лекарство'
    MEDICAL_PRODUCTS = 2, 'Медицинские изделие'
    COSMETICS = 3, 'Косметика'
    HYGIENE = 4, 'Гигиена'
    SUPPLEMENTS_VITAMINS = 5, 'Добавки и витамины'


class TypeCart(models.IntegerChoices):
    ACTIVE = 0, 'Активирована'
    BLOCKED = 1, 'Заблокирована'


class Goods(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name='price_goods_CK',
            ),
            models.CheckConstraint(
                check=models.Q(amount__gte=0),
                name='amount_goods_CK',
            ),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=256, verbose_name='Название товара')
    photo = models.ImageField(upload_to='goods/%Y/%m/%d/', default='default/photo_goods.png',
                              verbose_name='Фотография')
    available_delivery = models.BooleanField(default=False, verbose_name='Есть доставка')
    prescription_only = models.BooleanField(default=False, verbose_name='Только по рецепту')
    type_goods = models.PositiveSmallIntegerField(choices=TypeGoods.choices, default=TypeGoods.OTHER,
                                                  verbose_name='Тип товара')
    goods_info = models.CharField(max_length=2048, verbose_name='Информарция о товаре')
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Цена')
    amount = models.SmallIntegerField(default=0, verbose_name='Количество товаров')

    objects = models.Manager()


class Promotion(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(promotion_percentage__gte=10) &
                       models.Q(promotion_percentage__lte=90)),
                name='promotion_percentage_CK',
            ),
        ]
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    promotions_goods_id = models.ForeignKey(Goods,
                                            on_delete=models.CASCADE,
                                            related_name='promotions_goods_fk',
                                            verbose_name='Скидка на товар')
    time_end_promotion = models.DateTimeField(verbose_name='Время конца скидки')
    promotion_percentage = models.SmallIntegerField(verbose_name='Процент скидки')

    objects = models.Manager()


class PromoCode(models.Model):
    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    promo_code_goods_id = models.ForeignKey(Goods,
                                            on_delete=models.CASCADE,
                                            related_name='promo_code_goods_fk',
                                            verbose_name='Промокод на товар')
    promo_code = models.CharField(max_length=64, verbose_name='Промокод')
    is_used = models.BooleanField(default=False, verbose_name='Ипользован')
    time_action = models.DateTimeField(verbose_name='Время действия')

    objects = models.Manager()


class GoodsRating(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(grade__gte=0.0) &
                       models.Q(grade__lte=5.0)),
                name='grade_CK',
            ),
        ]
        unique_together = (('rating_goods', 'user_grade'),)
        verbose_name = 'Оценка товара'
        verbose_name_plural = 'Оценки товарав'

    rating_goods = models.ForeignKey(Goods,
                                     on_delete=models.CASCADE,
                                     related_name='rating_goods_fk',
                                     verbose_name='Оцениваемый товар')
    user_grade = models.ForeignKey(AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='user_grade_fk',
                                   verbose_name='Оценка пользователя')
    grade = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Оценка')

    objects = models.Manager()


class GoodsReview(IMessage):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    goods_review = models.ForeignKey(Goods,
                                     on_delete=models.CASCADE,
                                     related_name='goods_review_fk',
                                     verbose_name='Отзыв')


class LoyaltyCard(models.Model):
    class Meta:
        verbose_name = 'Карта лояльности'
        verbose_name_plural = 'Карты лояльности'

    user_card = models.ForeignKey(AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='user_card_fk',
                                  verbose_name='Карта пользователя')
    card_status = models.PositiveSmallIntegerField(choices=TypeCart.choices, default=TypeCart.ACTIVE,
                                                   verbose_name='Тип товара')
    bonuses = models.IntegerField(default=0, verbose_name='Количество бонусов')

    objects = models.Manager()


class ShoppingCart(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='amount_CK',
            ),
        ]
        unique_together = (('goods_cart', 'user_cart'),)
        verbose_name = 'Товар в карзине'
        verbose_name_plural = 'Товары в карзинах'

    goods_cart = models.ForeignKey(Goods,
                                   on_delete=models.CASCADE,
                                   related_name='goods_cart_fk',
                                   verbose_name='Товар в корзине')
    user_cart = models.ForeignKey(AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='user_cart_fk',
                                  verbose_name='Корзина пользователя')
    amount = models.SmallIntegerField(default=1, verbose_name='Количество в корзине')

    objects = models.Manager()


class Purchase(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(for_money__gte=0),
                name='price_purchase_CK',
            ),
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='amount_purchase_CK',
            ),
        ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    user_buy = models.ForeignKey(Goods,
                                 on_delete=models.CASCADE,
                                 related_name='user_buy_fk',
                                 verbose_name='Покупатель')
    goods_buy = models.ForeignKey(Goods,
                                  on_delete=models.CASCADE,
                                  related_name='goods_buy_fk',
                                  verbose_name='Покупаемый товар')
    date_buy = models.DateField(verbose_name='Время покупки')
    for_money = models.DecimalField(max_digits=10, decimal_places=2,
                                    verbose_name='Купил за сумму')
    amount = models.SmallIntegerField(default=1, verbose_name='Количество купленного товара')

    objects = models.Manager()

