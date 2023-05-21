# Supervision2023

### Authors:
- Mikołaj Gałkowski
- Hubert Bujakowski
- Maja Andrzejczuk
- Łukasz Tomaszewski
- Wiktor Jakubowski
- Andrzej Pióro
---

## Cel zadania 
Zadanie polegało na stworzeniu webscappera pobierającego oferty z portalów ogłoszeniowych. Następnie pobrane oferty należało sklasyfikować przy pomocy stworzonego modelu jako oszustwa i prawdziwe ogłoszenia. Została przygotowana aplikacja webowa umożliwiająca przeglądanie pobranych ogłoszeń oraz ich analizę.


### Instalacja pakietów
Wymagane pakiety znajdują się w pliku `requirements.txt`. Rekomendujemy używanie `conda` i użycie komendy: `conda create --name <env> --file requirements.txt`.

---
### Struktura plików
- backend:
  - base, job_analyzer, supervision_app - foldery związane z aplikacją webową napisaną w django
  - model - zawiera wszystkie pliki potrzebne do uruchomienia modelu:
    - feature_engineering - tworzenie nowych cech na podstawie tekstu i dat
    - modeling - trenowanie i ewaluacja modelu
    - preprocessing - czyszczenie danych i przygotowanie ich do modelu
    - pipeline - połaczenie preprocessingu i inżynierii cech
- data - zawiera dane, które zostały przygotowane przez scaprery i użyte w procesie uczenia modelu
- scrapers - zawiera funkcje umożliwiajace web scraping  poszczególnych portali
- script.sh - skrypt umożliwiający automatyczne uruchamianie scrapingu i evaluacje modelu na zescrapowanych danych (należy skonfigurować ścieżki)


### Konteneryzacja
Cała aplikacja jest skonteneryzowana w postaci kontenerów Dockerowych. Dzięki temu, cała aplikacja jest gotowa do użytku. Aby to wykonać, należy następującymi komendami stworzyć i uruchomić zbudowany obraz:

### Celery commands
```
docker run -d -p 6379:6379 redis

celery -A supervision_app worker  --loglevel=INFO -E
```

Also you need to remember to add script to crontab. It should be run every 10 minutes.
```
