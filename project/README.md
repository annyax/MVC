# Budzet Domowy - system monitorowania wydatkow domowych

## Spis tresci

1. [Opis projektu](#opis-projektu)
2. [Funkcjonalnosci](#funkcjonalnosci)
3. [Struktura MVC/MVT](#struktura-mvcmvt)
4. [Technologie i biblioteki](#technologie-i-biblioteki)
5. [Uruchomienie lokalne](#uruchomienie-lokalne)
6. [Uruchomienie w Dockerze](#uruchomienie-w-dockerze)
7. [Testy](#testy)
8. [Przykladowe dane](#przykladowe-dane)

## Opis projektu

Projekt realizuje temat: **System monitorowania wydatkow domowych**. Aplikacja zostala napisana w Django i pozwala prowadzic liste domowych wydatkow, przypisywac je do kategorii i metod platnosci oraz filtrowac dane na liscie.

## Funkcjonalnosci

- wyswietlanie listy wydatkow w ostylowanej tabeli,
- dodawanie nowych wydatkow,
- edycja istniejacych wydatkow,
- usuwanie wydatkow,
- widok szczegolow pojedynczego wydatku,
- wyszukiwanie po nazwie wydatku,
- filtrowanie po kategorii i metodzie platnosci,
- walidacja po stronie klienta przez atrybuty HTML,
- walidacja po stronie serwera przez Django ModelForm i walidatory modelu,
- migracje Django tworzace baze SQLite i dane startowe,
- przykladowe testy jednostkowe Django,
- konfiguracja Docker.

## Struktura MVC/MVT

- **Model**: `expenses/models.py`
  - `Expense`: glowny model wydatku (`title`, `amount`, `spent_on`, `note`),
  - `Category`: dodatkowy model kategorii wydatku,
  - `PaymentMethod`: dodatkowy model metody platnosci.
- **Relacje**:
  - jeden `Category` ma wiele `Expense`,
  - jeden `PaymentMethod` ma wiele `Expense`.
- **Kontroler / View w Django**: `expenses/views.py`
  - obsluga zadan HTTP,
  - obsluga formularzy,
  - zapis, edycja, usuwanie i filtrowanie rekordow.
- **Widok / Template**: `expenses/templates/expenses/`
  - lista wydatkow,
  - formularz dodawania i edycji,
  - widok szczegolow pojedynczego obiektu.

Django formalnie korzysta z nazwy MVT (Model-View-Template), ale struktura odpowiada wymaganiom MVC: model jest w `models.py`, logika kontrolera w `views.py`, a warstwa prezentacji w szablonach HTML.

## Technologie i biblioteki

- Python 3.12,
- Django,
- SQLite,
- Docker.

## Uruchomienie lokalne

1. Przejdz do katalogu projektu:

```bash
cd project
```

2. Utworz i aktywuj srodowisko wirtualne:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Zainstaluj wymagane paczki:

```bash
pip install -r requirements.txt
```

4. Uruchom aplikacje:

```bash
python manage.py migrate
python manage.py runserver
```

5. Otworz w przegladarce:

```text
http://127.0.0.1:8000
```

## Uruchomienie w Dockerze

```bash
docker compose up --build
```

Aplikacja bedzie dostepna pod adresem:

```text
http://127.0.0.1:5000
```

## Testy

Po zainstalowaniu zaleznosci uruchom:

```bash
python manage.py test
```

## Przykladowe dane

Przykladowe dane znajduja sie w pliku:

```text
data/sample_expenses.csv
```

Dodatkowo migracje Django tworza baze `db.sqlite3` i dodaja kilka rekordow startowych.
