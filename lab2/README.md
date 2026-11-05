# Prosty symulator skrzyni biegów

Program symuluje automatyczną skrzynię biegów w np. samochodzie - dobiera bieg na podstawie różnych czynników.

## Wejścia

- Pedał gazu - ułamek od 0 (nie wciśnięty) do 1 (gaz do dechy)
  - 0 - hamowanie
  - 0.2 - utrzymanie prędkości
  - 0.5 - przyspieszanie
  - 0.9 - turbo

- Obroty silnika - od 0 do 6000
  - 0 - silnik gaśnie/zgasł
  - 500 - obroty bardzo niskie
  - 800 - obroty jałowe
  - 1800 - obroty optymalne
  - 3500 - obroty wysokie
  - 5000 - obroty zbyt wysokie

- Aktualne przyspieszenie - od -3 do +3 m/s^2
  - -3 - gwałtowne hamowanie
  - -1.5 - hamowanie
  - 0 - utrzymanie prędkości
  - 1.5 - rozpędzanie
  - 3 - gwałtowne rozpędzanie

## Wyjście

- Co zrobić z biegiem: zrzucić na luz (0), zrzucić o jeden bieg (0.5), pozostać na aktualnym biegu (0.75), wrzucić bieg wyżej (1)

## Wymagania

- Python 3.x
- Biblioteka `scikit-fuzzy`
- Biblioteka `numpy`
- Zależności do powyższych: `scipy`, `networkx`

## Instalacja

Aby zainstalować zależności do tego programu, należy w konsoli wpisać:

```bash
pip install scikit-fuzzy
pip install numpy
pip install scipy networkx
```

## Uruchomienie

Aby uruchomić program wpisz w konsoli

```bash
python main.py
```