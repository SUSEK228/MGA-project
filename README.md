# MGA-project Task Manager

## Opis Projektu
Task Manager to aplikacja webowa do zarządzania zadaniami. Jest napisana w Django 5.2.1 z wykorzystaniem Django REST Framework oraz PostgreSQL. Umożliwia rejestrację użytkowników, uwierzytelnianie JWT, przydzielanie i edycję zadań, kontrolę uprawnień oraz śledzenie historii zmian.

## Instrukcja uruchomienia aplikacji

### Wymagane:
- Docker
- Docker Compose

### Klonowanie Repozytorium:
- git clone ```https://github.com/SUSEK228/MGA-project.git```
- cd mga-project/task_manager

### Budowanie i Uruchamianie kontenerów:
- ```docker-compose build```
- ```docker-compose up -d ```

### Migracje bazy danych
- ```docker-compose exec web python manage.py makemigrations```
- ```docker-compose exec web python manage.py migrate```

### Tworzenie superużytkownika
- ```docker-compose exec web python manage.py createsuperuser```

### Sprawdzenie działania
- ```http://localhost:8000/api/```

## Sposób użycia aplikacji:
- Aplikację można używać za pomocą przeglądarki internetowej.
- Po uruchomieniu serwera aplikacji, interfejs API dostępny jest pod adresem: ```http://localhost:8000/```
### Używając curl
*można uruchomić w CMD/Powershell lub w terminalu VS Code*

#### Rejestracja i logowanie 
- ```curl -X POST "http://localhost:8000/api/register/" -H "Content-Type: application/json" -d "{\"username\": \"uzytkownik\", \"password\": \"haslo\"}"```
#### Logowanie (JWT)
- ```curl -X POST "http://localhost:8000/api/token/" -H "Content-Type: application/json" -d "{\"username\": \"uzytkownik\", \"password\": \"haslo\"}"```
#### Odświeżenie tokena
- ```curl -X POST "http://localhost:8000/api/token/refresh/" -H "Content-Type: application/json" -d "{\"refresh\": \"<REFRESH_TOKEN>\"}"```
#### pobranie listy zadań
- ```curl -X GET "http://localhost:8000/api/tasks/" -H "Authorization: Bearer <TOKEN>"```
#### Filtrowanie po statusie
- ```curl -X GET "http://localhost:8000/api/tasks/?status=Nowy" -H "Authorization: Bearer <TOKEN>"```
#### Dodanie zadania
- ```curl -X POST "http://localhost:8000/api/tasks/" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"name\": \"Zadanie testowe\", \"status\": \"Nowy\"}"```
#### edycja zadania (przykładowo zadanie o id 1)
- ```curl -X PATCH "http://localhost:8000/api/tasks/1/" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"status\": \"W toku\"}"```
#### usunięcie zadania (przykładowo zadanie o id 1)
- ```curl -X DELETE "http://localhost:8000/api/tasks/1/" -H "Authorization: Bearer <TOKEN>"```
#### Historia zmian zadania (przykładowo zadanie o id 1)
- ```curl -X GET "http://localhost:8000/api/tasks/1/history/" -H "Authorization: Bearer <TOKEN>"```

## System uprawnień
Tworzenie/Edycja/Usuwanie możliwa tylko dla
- autora (created_by)
- przypisanego użytkownika (assigned_user)
- administratora (is_staff)

## Testowanie
Testy są uruchamiane przez komendę:
- ```docker-compose exec web pytest```

## Dodatkowe Informacje

## Autor
Paweł Kulesza

*Projekt wykonany jako zadanie rekrutacyjne dla MGA*