import pytest
from django.test import TestCase, Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.models import CustomUser


def test_register_get():
    url = reverse('register')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_post_valid_data():
    url = reverse('register')
    client = Client()
    data = {
        'username': 'test',
        'email': 'test@example.com',
        'password1': 'newpassword123',
        'password2': 'newpassword123',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_register_post_invalid_data():
    url = reverse('register')
    client = Client()
    data = {
        'username': 'test',
        'email': 'test@example.com',
        'password1': 'newpassword123',
        'password2': 'wrongpassword123',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors


def test_login_get():
    url = reverse('login')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post_valid_data(user):
    url = reverse('login')
    client = Client()
    client.force_login(user)
    data = {
        'username': user.username,
        'password': 'secret123'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('boardgames_list')


@pytest.mark.django_db
def test_login_post_invalid_data():
    url = reverse('login')
    client = Client()
    data = {
        'username': 'testuser',
        'password': 'wrongpassword123'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['form'].errors
    assertTemplateUsed(response, 'accounts/form.html')


@pytest.mark.django_db
def test_logout_get(user):
    url = reverse('login')
    client = Client()
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('landing_page')
