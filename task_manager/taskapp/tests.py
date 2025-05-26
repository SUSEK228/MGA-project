import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Task

# czy zalogowany uzytkownik moze stworzyc zadanie
@pytest.mark.django_db
def test_user_can_create_task():
    user = User.objects.create_user(username="tester", password="haslo123")
    
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/tasks/", {
        "name": "Testowe zadanie",
        "description": "To tylko test",
        "status": "Nowy"
    }, format='json')

    assert response.status_code == 201
    assert Task.objects.count() == 1
    task = Task.objects.first()
    assert task.created_by == user

# sprawdzenie czy obcy moze edytowac zadanie
@pytest.mark.django_db
def test_other_user_cant_edit_task():
    owner = User.objects.create_user(username="owner", password="haslo123")
    user2 = User.objects.create_user(username="intruz", password="haslo456")

    task = Task.objects.create(name="zadanie", created_by=owner, status="Nowy")

    client = APIClient()
    client.force_authenticate(user=user2)

    response = client.patch(f"/api/tasks/{task.id}/", {
        "status": "Rozwiązany"
    }, format='json')

    assert response.status_code == 403  

# sprawdzenie czy osoba przypisana do zadanie moze je edytowac
@pytest.mark.django_db
def test_assigned_user_can_edit_task():
    creator = User.objects.create_user(username="creator", password="haslo123")
    assign = User.objects.create_user(username="user", password="haslo456")

    task = Task.objects.create(
        name="Zadanie do wykonania",
        created_by=creator,
        assigned_user=assign,
        status="Nowy"
    )

    client = APIClient()
    client.force_authenticate(user=assign)

    response = client.patch(f"/api/tasks/{task.id}/", {
        "status": "W_toku"
    }, format='json')

    assert response.status_code == 200
    task.refresh_from_db()
    assert task.status == "W_toku"

# sprawdzenie czy po edycji zadanie jest wpis do historii
@pytest.mark.django_db
def test_task_log_changed_on_update():
    user = User.objects.create_user(username="tester", password="haslo123")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/tasks/", {
        "name": "Zadanie testowe",
        "status": "Nowy"
    }, format='json')
    task_id = response.data["id"]

    client.patch(f"/api/tasks/{task_id}/", {
        "status": "W_toku"
    }, format='json')

    history_response = client.get(f"/api/tasks/{task_id}/history/")
    assert history_response.status_code == 200
    assert len(history_response.data) == 1
    assert history_response.data[0]["old_data"]["status"] == "Nowy"
    assert history_response.data[0]["new_data"]["status"] == "W_toku"
    
# sprawdzenie czy niezalogowany uzytkwonik moze zrobic zadanie 
@pytest.mark.django_db
def test_not_login_user_cant_post_task():
    client = APIClient() 

    response = client.post("/api/tasks/", {
        "name": "Zadanie nieautoryzowane",
        "status": "Nowy"
    }, format='json')

    assert response.status_code == 401  # brak dostepu 

# sprawdzenie czy autor moze usunac swoje zadanie
@pytest.mark.django_db
def test_can_creator_delete_task():
    user = User.objects.create_user(username="autor", password="123")
    task = Task.objects.create(name="Do usunięcia", created_by=user)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == 204  
    assert Task.objects.count() == 0

# sprawdzenie czy obcy uzytkwonik moze usunac to zadanie
@pytest.mark.django_db
def test_can_other_user_delete_task():
    owner = User.objects.create_user(username="właściciel", password="123")
    other = User.objects.create_user(username="nie_właściciel", password="456")
    task = Task.objects.create(name="Chronione", created_by=owner)

    client = APIClient()
    client.force_authenticate(user=other)

    response = client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == 403 
    assert Task.objects.count() == 1
