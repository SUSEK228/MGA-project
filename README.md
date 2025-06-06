# Task Manager – Projekt MGA

## Opis Projektu
Task Manager to aplikacja webowa do zarządzania zadaniami. Jest napisana w Django 5.2.1 z wykorzystaniem Django REST Framework oraz PostgreSQL. Umożliwia rejestrację użytkowników, uwierzytelnianie JWT, przydzielanie i edycję zadań, kontrolę uprawnień oraz śledzenie historii zmian.

## Technologie
- Django 5.2.1
- Django REST Framework
- PostgreSQL
- JWT (JSON Web Token)
- Docker / Docker Compose
- Gunicorn (serwer WSGI)

## Struktura projektu
```
MGA-project/
├── README.md                 # Plik dokumentacji projektu
├── task_manager/             # Główna aplikacja Django
│   ├── manage.py             # Główny plik uruchamiający Django
│   ├── Dockerfile            # Konfiguracja kontenera aplikacji
│   ├── docker-compose.yml    # Konfiguracja usług (Django + Postgres)
│   ├── requirements.txt      # Lista zależności Pythona
│   ├── pytest.ini            # Konfiguracja dla pytest
│   ├── staticfiles/          # Zebrane pliki statyczne
│   ├── task_manager/         # Konfiguracja projektu Django (settings, urls)
│   └── taskapp/              # Aplikacja do zarządzania zadaniami (models, views, serializers, tests)
```

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
*Komendy można uruchomić w CMD/Powershell lub w terminalu VS Code*

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

## Endpointy API 
- `POST /api/register/` – rejestracja
- `POST /api/token/` – logowanie (JWT)
- `POST /api/token/refresh/` – odświeżenie tokena
- `GET /api/tasks/` – lista zadań
- `GET /api/tasks/?status=Nowy` – filtrowanie zadań po statusie (w przykładzie filtrowanie po Nowy)
- `POST /api/tasks/` – tworzenie zadania
- `PATCH /api/tasks/<id>/` – edycja zadania
- `DELETE /api/tasks/<id>/` – usunięcie zadania
- `GET /api/tasks/<id>/history/` – historia zmian zadania

## System uprawnień
Tworzenie/Edycja/Usuwanie możliwa tylko dla
- autora (created_by)
- przypisanego użytkownika (assigned_user)
- administratora (is_staff)

Przykład:
- Użytkownik 1 tworzy zadanie i przypisuje do niego użytkownika 2. Zadanie może edytować tylko użytkownik 1, 2 lub administrator.
Każdy użytkownik może tworzyć zadania, ale edytować i usuwać tylko te, które stworzył lub do których został przypisany.
Osoby niezalogowane mogą jedynie przeglądać listę zadań.

## Testowanie
Testy są uruchamiane przez komendę:
- ```docker-compose exec web pytest```

## Autor
Paweł Kulesza

*Projekt wykonany jako zadanie rekrutacyjne dla MGA*