import pytest
from django.test import TestCase, Client
from django.urls import reverse
from bs4 import BeautifulSoup

from shop.models import Boardgame


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
def test_boardgame_add_view_superuser(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_add')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_boardgame_add_view_not_superuser(user):
    client = Client()
    client.force_login(user)
    url = reverse('boardgame_add')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_boardgame_add_view_anonymous():
    client = Client()
    url = reverse('boardgame_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_boardgame_add_view_post_superuser(superuser, publisher, category):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_add')
    data = {
        'name': 'New Boardgame',
        'price': '29.99',
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
def test_boardgame_add_view_post_invalid_data(superuser, publisher, category):
    client = Client()
    client.force_login(superuser)
    url = reverse('boardgame_add')
    data = {
        'name': '',
        'price': '29.99',
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


