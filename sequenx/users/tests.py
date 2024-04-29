import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from .models import UserProfile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    return UserProfile.objects.create(email='uzair@example.com', password='password123@')

def test_register_user(api_client):
    url = reverse('api:register')
    data = {'email': 'test@example.com', 'password': 'password'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert UserProfile.objects.filter(email='test@example.com').exists()

def test_login(api_client, create_user):
    url = reverse('api:login')
    data = {'email': 'uzair@example.com', 'password': 'password123@'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

def test_profile_retrieve(api_client, create_user):
    url = reverse('api:profile')
    api_client.force_authenticate(create_user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['email'] == 'uzair@example.com'


if __name__ == '__main__':
    pytest.main()
