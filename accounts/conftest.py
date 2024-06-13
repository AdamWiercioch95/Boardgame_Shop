import pytest

from accounts.models import CustomUser


@pytest.fixture
def user():
    user = CustomUser.objects.create(username='test', email='test@op.pl')
    user.set_password('secret123')
    user.save()
    return user
