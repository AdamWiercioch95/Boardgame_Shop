from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg, Sum, F

from accounts.models import CustomUser


class Boardgame(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Price')
    description = models.TextField(verbose_name='Description')
    min_players_age = models.IntegerField(validators=[MinValueValidator(2)], verbose_name='Min. Players Age')
    min_players = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Min. Players Number')
    max_players = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Max. Players Number')
    min_game_time = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Min. Game Time')
    max_game_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
        verbose_name='Max. Game Time')
    categories = models.ManyToManyField('Category', verbose_name='Categories')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, verbose_name='Publisher')

    class Meta:
        ordering = ['name']

    def avg_rating(self):
        avg_rating = self.review_set.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 2)
        return "No Review Added"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


RATING = (
    (1, '1 star'),
    (2, '2 star'),
    (3, '3 star'),
    (4, '4 star'),
    (5, '5 star'),
)


class Review(models.Model):
    rating = models.IntegerField(choices=RATING, default=0)
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(Boardgame, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']
        unique_together = ('user', 'boardgame')

    def __str__(self):
        return f'{self.boardgame} - {self.rating}'


class CartBoardgame(models.Model):
    boardgame = models.ForeignKey(Boardgame, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total(self):
        return self.quantity * self.boardgame.price


class Cart(models.Model):
    boardgames = models.ManyToManyField(Boardgame, through='CartBoardgame')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def total(self):
        result = self.cartboardgame_set.aggregate(
            total=Sum(F('quantity') * F('boardgame__price'))
        )['total'] or 0
        return round(result, 2)


class OrderBoardgame(models.Model):
    boardgame = models.ForeignKey(Boardgame, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total(self):
        return self.quantity * self.boardgame.price


class Order(models.Model):
    boardgame = models.ManyToManyField(Boardgame, through='OrderBoardgame')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def total(self):
        result = self.orderboardgame_set.aggregate(
            total=Sum(F('quantity') * F('boardgame__price'))
        )['total'] or 0
        return round(result, 2)
