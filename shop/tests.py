import pytest
from django.test import TestCase, Client
from django.urls import reverse
from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed

from shop.models import Boardgame, Cart, CartBoardgame, Order, OrderBoardgame, Review
from shop.forms import CustomUserForm


# landing page
@pytest.mark.django_db
def test_landing_page():
    url = reverse('landing_page')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


# ------------------------------------------------------------------------------------------------------ boardgame list
@pytest.mark.django_db
def test_boardgame_list(boardgame):
    url = reverse('boardgames_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["boardgame_list"]) == 1
    assert response.context["boardgame_list"][0] == boardgame


@pytest.mark.django_db
def test_boardgame_list_superuser(superuser, boardgame):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgames_list')
    response = client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')
    add_boardgame_button = soup.find('a', text='Add boardgame')
    edit_boardgame_button = soup.find('a', text='Edit')
    delete_boardgame_button = soup.find('a', text='Delete')
    assert add_boardgame_button is not None
    assert edit_boardgame_button is not None
    assert delete_boardgame_button is not None


@pytest.mark.django_db
@pytest.mark.parametrize(
    'query', ['Test', 'test', 'es', 'TeSt']
)
def test_boardgame_list_search(boardgame, query):
    url = reverse('boardgames_list') + f'?q={query}'
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["boardgame_list"]) == 1
    assert response.context["boardgame_list"][0] == boardgame


# ---------------------------------------------------------------------------------------------------- boardgame detail
@pytest.mark.django_db
def test_boardgame_detail_not_authenticated(boardgame):
    url = reverse('boardgame_details', kwargs={'pk': boardgame.pk})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')
    your_review_button = soup.find('a', text='Your Review')

    assert your_review_button is None
    assert 'is_reviewed' in response.context
    assert response.context["is_reviewed"] is False


@pytest.mark.django_db
def test_boardgame_detail_authenticated_no_review(user, boardgame):
    client = Client()
    client.force_login(user)
    url = reverse('boardgame_details', kwargs={'pk': boardgame.pk})
    response = client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')
    add_review_button = soup.find('a', text='Add Review')
    your_review_button = soup.find('a', text='Your Review')

    assert add_review_button is not None
    assert your_review_button is None
    assert 'is_reviewed' in response.context
    assert response.context["is_reviewed"] is False


@pytest.mark.django_db
def test_boardgame_detail_authenticated_with_review(user, boardgame, review):
    client = Client()
    client.force_login(user)
    url = reverse('boardgame_details', kwargs={'pk': boardgame.pk})
    response = client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')
    add_review_button = soup.find('a', text='Add Review')
    your_review_button = soup.find('a', text='Your Review')

    assert add_review_button is None
    assert your_review_button is not None
    assert 'is_reviewed' in response.context
    assert response.context["is_reviewed"] is True


# ------------------------------------------------------------------------------------------------------- boardgame add
@pytest.mark.django_db
def test_boardgame_add_superuser(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_add')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_boardgame_add_not_superuser(user):
    client = Client()
    client.force_login(user)
    url = reverse('boardgame_add')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_boardgame_add_anonymous():
    client = Client()
    url = reverse('boardgame_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_boardgame_add_post_superuser(superuser, publisher, category):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_add')
    data = {
        'name': 'New Boardgame',
        'price': 29.99,
        'description': 'A fun new game',
        'min_players_age': 10,
        'min_players': 2,
        'max_players': 4,
        'min_game_time': 30,
        'max_game_time': 60,
        'publisher': publisher.pk,
        'categories': [category.pk],
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('boardgames_list')
    assert Boardgame.objects.filter(name='New Boardgame').exists()


@pytest.mark.django_db
def test_boardgame_add_post_invalid_data(superuser, publisher, category):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_add')
    data = {
        'name': '',
        'price': 29.99,
        'description': 'A fun new game',
        'min_players_age': 10,
        'min_players': 2,
        'max_players': 4,
        'min_game_time': 30,
        'max_game_time': 60,
        'publisher': publisher.pk,
        'categories': [category.pk],
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert 'name' in response.context['form'].errors
    assert response.context['form'].errors['name'] == ['This field is required.']


# ---------------------------------------------------------------------------------------------------- boardgame update
@pytest.mark.django_db
def test_boardgame_update_not_superuser(user, boardgame):
    client = Client()
    client.force_login(user)
    url = reverse('boardgame_update', kwargs={'pk': boardgame.pk})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_boardgame_update_superuser(superuser, boardgame):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_update', kwargs={'pk': boardgame.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_boardgame_update_invalid_data(superuser, boardgame, category, publisher):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_update', kwargs={'pk': boardgame.pk})
    data = {
        'name': '',
        'price': 29.99,
        'description': 'Test description',
        'min_players_age': 3,
        'min_players': 2,
        'max_players': 4,
        'min_game_time': 30,
        'max_game_time': 60,
        'categories': category.pk,
        'publisher': publisher.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert 'name' in response.context['form'].errors
    assert response.context['form'].errors['name'] == ['This field is required.']


@pytest.mark.django_db
def test_boardgame_update_view_valid_data(superuser, boardgame, category, publisher):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_update', kwargs={'pk': boardgame.pk})
    data = {
        'name': 'Updated Game',
        'price': 39.99,
        'description': 'Updated description',
        'min_players_age': 3,
        'min_players': 2,
        'max_players': 4,
        'min_game_time': 30,
        'categories': category.pk,
        'publisher': publisher.pk
    }
    response = client.post(url, data)
    assert response.status_code == 302


# ---------------------------------------------------------------------------------------------------- boardgame delete
@pytest.mark.django_db
def test_boardgame_delete_superuser(superuser, boardgame):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_delete', kwargs={'pk': boardgame.pk})

    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'shop/boardgame_confirm_delete.html')
    assert 'title' in response.context
    assert response.context['title'] == 'Delete Boardgame'

    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('boardgames_list')
    assert not Boardgame.objects.filter(pk=boardgame.pk).exists()


@pytest.mark.django_db
def test_boardgame_delete_not_superuser(user, boardgame):
    client = Client()
    client.force_login(user)
    url = reverse('boardgame_delete', kwargs={'pk': boardgame.pk})

    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_boardgame_delete_anonymous(boardgame):
    client = Client()
    url = reverse('boardgame_delete', kwargs={'pk': boardgame.pk})

    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


# ---------------------------------------------------------------------------------------------------------- cart list
@pytest.mark.django_db
def test_cart_list_authenticated(user):
    client = Client()
    client.force_login(user)
    url = reverse('cart_list')

    response = client.get(url)
    assert response.status_code == 200
    assert 'cart' in response.context
    cart = response.context['cart']
    assert cart.user == user


@pytest.mark.django_db
def test_cart_list_anonymous():
    client = Client()
    url = reverse('cart_list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


# ----------------------------------------------------------------------------------------------- add boardgame to cart
@pytest.mark.django_db
def test_add_boardgame_to_cart_authenticated(user, boardgame, cart):
    client = Client()
    client.force_login(user)
    url = reverse('add_boardgame_to_cart', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('cart_list')
    assert CartBoardgame.objects.filter(cart=cart, boardgame=boardgame).exists()


@pytest.mark.django_db
def test_add_boardgame_to_cart_cart_item_increment(user, boardgame, cart):
    client = Client()
    client.force_login(user)
    cart.boardgames.add(boardgame)

    url = reverse('add_boardgame_to_cart', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('cart_list')

    cart_item = CartBoardgame.objects.get(cart=cart, boardgame=boardgame)
    assert cart_item.quantity == 2


@pytest.mark.django_db
def test_add_boardgame_to_cart_anonymous(boardgame):
    client = Client()
    url = reverse('add_boardgame_to_cart', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


# ------------------------------------------------------------------------------------------ delete boardgame from cart
@pytest.mark.django_db
def test_delete_boardgame_from_cart_authenticated(user, boardgame, cart):
    client = Client()
    client.force_login(user)
    cart_item = CartBoardgame.objects.create(boardgame=boardgame, cart=cart, quantity=2)

    url = reverse('delete_boardgame_from_cart', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('cart_list')

    cart_item.refresh_from_db()
    assert cart_item.quantity == 1


@pytest.mark.django_db
def test_delete_boardgame_from_cart_last_item(user, boardgame, cart):
    client = Client()
    client.force_login(user)
    CartBoardgame.objects.create(boardgame=boardgame, cart=cart, quantity=1)

    url = reverse('delete_boardgame_from_cart', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('cart_list')
    assert not CartBoardgame.objects.filter(boardgame=boardgame, cart=cart).exists()


# ---------------------------------------------------------------------------------------------------------- make order
@pytest.mark.django_db
def test_make_order_authenticated(user, boardgame, cart):
    client = Client()
    client.force_login(user)
    CartBoardgame.objects.create(boardgame=boardgame, cart=cart, quantity=1)

    url = reverse('make_order')
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('cart_list')

    assert Order.objects.filter(user=user).exists()

    order = Order.objects.get(user=user)
    order_boardgame = OrderBoardgame.objects.get(order=order)
    assert order_boardgame.boardgame == boardgame
    assert order_boardgame.quantity == 1

    assert not CartBoardgame.objects.filter(cart=cart).exists()


@pytest.mark.django_db
def test_make_order_empty_cart(user):
    client = Client()
    client.force_login(user)
    Cart.objects.create(user=user)

    url = reverse('make_order')
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('cart_list')
    assert not Order.objects.filter(user=user).exists()


# ---------------------------------------------------------------------------------------------------------- order list
@pytest.mark.django_db
def test_orders_list_authenticated(user, order):
    client = Client()
    client.force_login(user)

    url = reverse('orders_list')
    response = client.get(url)

    assert response.status_code == 200

    orders = response.context['object_list']
    assert len(orders) == 1


@pytest.mark.django_db
def test_orders_list_unauthenticated():
    client = Client()
    url = reverse('orders_list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


# ------------------------------------------------------------------------------------------------------- order details
@pytest.mark.django_db
def test_order_detail_authenticated(user, order, order_boardgame):
    client = Client()
    client.force_login(user)
    url = reverse('order_detail', kwargs={'pk': order.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert 'order' in response.context
    assert response.context['order'] == order
    assert 'object' in response.context
    assert order_boardgame in response.context['object'].orderboardgame_set.all()


@pytest.mark.django_db
def test_order_detail_unauthenticated(order):
    client = Client()
    url = reverse('order_detail', kwargs={'pk': order.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


# ---------------------------------------------------------------------------------------------------------- review add
@pytest.mark.django_db
def test_review_add_authenticated(user, boardgame):
    client = Client()
    client.force_login(user)
    url = reverse('review_add', kwargs={'boardgame_pk': boardgame.pk})
    data = {
        'rating': 5,
        'comment': 'Great game!'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('boardgame_details', kwargs={'pk': boardgame.pk})
    assert Review.objects.filter(user=user, boardgame=boardgame).exists()


@pytest.mark.django_db
def test_review_add_unauthenticated(boardgame):
    client = Client()
    url = reverse('review_add', kwargs={'boardgame_pk': boardgame.pk})
    response = client.post(url)

    assert response.status_code == 302


# ------------------------------------------------------------------------------------------------------ review details
@pytest.mark.django_db
def test_review_detail_authenticated(user, review):
    client = Client()
    client.force_login(user)
    url = reverse('review_detail', kwargs={'pk': review.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert 'review' in response.context
    assert response.context['review'] == review


@pytest.mark.django_db
def test_review_detail_unauthenticated(review):
    client = Client()
    url = reverse('review_detail', kwargs={'pk': review.pk})
    response = client.get(url)

    assert response.status_code == 302


# ------------------------------------------------------------------------------------------------------- review update
@pytest.mark.django_db
def test_review_update_authenticated(user, review):
    client = Client()
    client.force_login(user)
    url = reverse('review_update', kwargs={'pk': review.pk})
    new_rating = 5
    new_comment = 'Awesome game!'
    data = {'rating': new_rating, 'comment': new_comment}
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('boardgame_details', kwargs={'pk': review.boardgame.pk})

    review.refresh_from_db()
    assert review.rating == new_rating
    assert review.comment == new_comment


@pytest.mark.django_db
def test_review_update_unauthenticated(client, review):
    url = reverse('review_update', kwargs={'pk': review.pk})
    response = client.get(url)

    assert response.status_code == 302


# ------------------------------------------------------------------------------------------------------- review delete
@pytest.mark.django_db
def test_review_delete_authenticated(user, review):
    client = Client()
    client.force_login(user)
    url = reverse('review_delete', kwargs={'pk': review.pk})
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('boardgame_details', kwargs={'pk': review.boardgame.pk})

    assert not Review.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_review_delete_unauthenticated(review):
    client = Client()
    url = reverse('review_delete', kwargs={'pk': review.pk})
    response = client.post(url)

    assert response.status_code == 302


# --------------------------------------------------------------------------------------------------------- review list
@pytest.mark.django_db
def test_reviews_list_with_review(boardgame, review):
    client = Client()
    url = reverse('reviews_list', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['object_list']) == 1
    assert response.context['boardgame'] == boardgame


@pytest.mark.django_db
def test_reviews_list_no_reviews(client, boardgame):
    url = reverse('reviews_list', kwargs={'boardgame_pk': boardgame.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['object_list']) == 0
    assert response.context['boardgame'] == boardgame


# -------------------------------------------------------------------------------------------------------- user profile
@pytest.mark.django_db
def test_user_profile_authenticated(user):
    client = Client()
    client.force_login(user)
    url = reverse('profile_view')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['user'] == user


@pytest.mark.django_db
def test_user_profile_not_authenticated():
    client = Client()
    url = reverse('profile_view')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url


# --------------------------------------------------------------------------------------------------- user profile edit
@pytest.mark.django_db
def test_edit_profile_get_authenticated(user):
    client = Client()
    client.force_login(user)
    url = reverse('profile_edit')
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.context['form'], CustomUserForm)


@pytest.mark.django_db
def test_edit_profile_post_authenticated(user):
    client = Client()
    client.force_login(user)
    url = reverse('profile_edit')
    data = {
        'first_name': 'TestFirstName',
        'last_name': 'TestLastName',
        'phone_number': '987654321',
        'city': 'TestCity',
        'street': 'TestStreet',
        'street_number': '123',
        'house_number': '12'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('profile_view')

    user.refresh_from_db()
    assert user.first_name == 'TestFirstName'
    assert user.last_name == 'TestLastName'
    assert user.phone_number == '987654321'
    assert user.address.city == 'TestCity'
    assert user.address.street == 'TestStreet'
    assert user.address.street_number == '123'
    assert user.address.house_number == '12'


@pytest.mark.django_db
def test_edit_profile_not_authenticated():
    client = Client()
    url = reverse('profile_edit')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url
