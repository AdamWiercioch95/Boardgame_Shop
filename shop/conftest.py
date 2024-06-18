import pytest

from accounts.models import CustomUser
from shop.models import Boardgame, Category, Publisher, Review, Cart, Order, CartBoardgame, OrderBoardgame


@pytest.fixture
def user():
    user = CustomUser.objects.create(username='test', email='test@op.pl')
    user.set_password('secret123')
    user.save()
    return user


@pytest.fixture
def superuser():
    superuser = CustomUser.objects.create_superuser(username='superuserTest', email='superusertest@op.pl')
    superuser.set_password('superuserSecret123')
    superuser.save()
    return superuser


@pytest.fixture
def category():
    return Category.objects.create(name='testCategory')


@pytest.fixture
def publisher():
    return Publisher.objects.create(name='testPublisher')


@pytest.fixture
def boardgame(category, publisher):
    boardgame = Boardgame.objects.create(
        name='test',
        price=100,
        description='test',
        min_players_age=3,
        min_players=2,
        max_players=4,
        min_game_time=30,
        max_game_time=90,
        publisher=publisher
    )
    boardgame.categories.add(category)
    return boardgame


@pytest.fixture
def review(user, boardgame):
    review = Review.objects.create(
        user=user,
        boardgame=boardgame,
        rating=5,
        comment='testComment'
    )
    return review


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


@pytest.fixture
def order(user):
    return Order.objects.create(user=user)


# @pytest.fixture
# def cart_boardgame(cart, boardgame):
#     return CartBoardgame.objects.create(cart=cart, boardgame=boardgame)


@pytest.fixture
def order_boardgame(order, boardgame):
    return OrderBoardgame.objects.create(order=order, boardgame=boardgame)

