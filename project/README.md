# Budzet Domowy - system monitorowania wydatkow domowych

## Spis tresci

1. [Opis projektu](#opis-projektu)
2. [Funkcjonalnosci](#funkcjonalnosci)
3. [Struktura MVC](#struktura-mvc)
4. [Technologie i biblioteki](#technologie-i-biblioteki)
5. [Uruchomienie lokalne](#uruchomienie-lokalne)
6. [Uruchomienie w Dockerze](#uruchomienie-w-dockerze)
7. [Testy](#testy)
8. [Przykladowe dane](#przykladowe-dane)

## Opis projektu

Projekt realizuje temat: **System monitorowania wydatkow domowych**. Aplikacja pozwala prowadzic liste domowych wydatkow, przypisywac je do kategorii i metod platnosci oraz filtrowac dane na liscie.

## Funkcjonalnosci

- wyswietlanie listy wydatkow w ostylowanej tabeli,
- dodawanie nowych wydatkow,
- edycja istniejacych wydatkow,
- usuwanie wydatkow,
- widok szczegolow pojedynczego wydatku,
- wyszukiwanie po nazwie wydatku,
- filtrowanie po kategorii i metodzie platnosci,
- walidacja po stronie klienta przez atrybuty HTML (`required`, `min`, `maxlength`),
- walidacja po stronie serwera w kontrolerze Flask,
- automatyczne utworzenie bazy SQLite i danych startowych,
- przykladowe testy jednostkowe,
- konfiguracja Docker.

## Struktura MVC

- **Model**: `app/models.py`
  - `Expense`: glowny model wydatku (`title`, `amount`, `spent_on`, `note`),
  - `Category`: dodatkowy model kategorii wydatku,
  - `PaymentMethod`: dodatkowy model metody platnosci.
- **Relacje**:
  - jeden `Category` ma wiele `Expense`,
  - jeden `PaymentMethod` ma wiele `Expense`.
- **Kontroler**: `app/controllers.py`
  - obsluga zadan HTTP,
  - walidacja danych,
  - zapis, edycja, usuwanie i filtrowanie rekordow.
- **Widok**: `app/templates/`
  - lista wydatkow,
  - formularz dodawania i edycji,
  - widok szczegolow pojedynczego obiektu.

## Technologie i biblioteki

- Python 3.12,
- Flask,
- Flask-SQLAlchemy,
- SQLite,
- pytest,
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
flask --app zad run
```

5. Otworz w przegladarce:

```text
http://127.0.0.1:5000
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
pytest
```

## Przykladowe dane

Przykladowe dane znajduja sie w pliku:

```text
data/sample_expenses.csv
```

Dodatkowo aplikacja przy pierwszym uruchomieniu sama tworzy baze `data/expenses.db` i dodaje kilka rekordow startowych.
