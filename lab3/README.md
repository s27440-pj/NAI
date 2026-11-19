# Rekomendacje filmów 🎥

## Działanie
Program wskazuje 5 polecanych i 5 odradzanych filmów dla wybranego (badanego) użytkownika.
Korzysta z danych zebranych w ankiecie, które zawierają nazwę użytkownika oraz listę filmów z ocenami.

W pierwszym kroku znajduje użytkowników, którzy obejrzeli minimum 5 takich samych filmów co badany użytkownik (nazywamy ich sąsiadami).

Następnie na podstawie metryki Pearsona lub Średniego błędu bezwzględnego (MAE) oblicza odległości między użytkownikami (na podstawie ocen tych samych filmów).

- jeśli jedna osoba jest jako jedyna bardzo blisko gustu badanej osoby (tj. wyliczona odległość między ocenami jest najmniejsza),
to poleca i odradza filmy tylko od tej osoby.
- jeśli zabraknie filmów do polecenia lub odradzenia - szuka wśród kolejnych sąsiadów.
- jeśli okaże się, że 2 osoby mają zbliżony gust do badanego (różnica w odległościach jest niewielka), to poleca / odradza
po 3 filmy od pierwszej osoby i po 2 od drugiej.
- jeli zabraknie filmów do polecenia od pierwszej osoby - uzupełnia brakujące filmy od drugiej osoby. W dalszej kolejności
uzupełnia od kolejnych sąsiadów.

## Wymagania
- Python 3.x
- numpy

## Uruchomienie
Aby uruchomić program, podaj w kodzie użytkownika i metrykę.
Następnie wpisz w konsoli:
```bash
python main.py
```