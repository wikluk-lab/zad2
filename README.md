# Sprawozdanie z Zadania 2 – Potok CI/CD w GitHub Actions

Repozytorium zawiera konfigurację automatycznego potoku CI/CD realizowanego za pomocą GitHub Actions. Celem zadania było automatyczne budowanie, testowanie pod kątem podatności (CVE) oraz publikacja wieloarchitekturowego obrazu aplikacji pogodowej z Zadania 1.

---

## Opis konfiguracji poszczególnych etapów

Potok został zdefiniowany w pliku .github/workflows/ci-cd.yml i składa się z następujących kroków:

### 1. Konfiguracja środowiska i pamięci podręcznej (Cache)
* Do budowania wykorzystano mechanizm **Docker Buildx** oraz emulator **QEMU**, co pozwala na kompilację obrazów na różne architektury procesorów.
* Wdrożono zewnętrzny mechanizm cache'owania warstw kontenera na Docker Hubie (wikluks2/app-cache). Dzięki temu ponowne uruchomienie potoku nie buduje wszystkiego od zera, co drastycznie skraca czas działania Actions.

### 2. Testy bezpieczeństwa (Skaner Trivy)
* Przed wrzuceniem obrazu do oficjalnego rejestru, kontener jest prześwietlany skanerem **Trivy** pod kątem krytycznych podatności (HIGH,CRITICAL).
* Zgodnie z wytycznymi, potok ma ustawiony parametr exit-code: '1'. Jeśli skaner wykryje niebezpieczne pakiety, działanie całego potoku zostaje natychmiast przerwane, a obraz nie trafi do sieci.
* **Rozwiązanie problemów z lukami:** Podczas pierwszych uruchomień Trivy zablokował potok z powodu luk wykrytych w domyślnych pakietach Pythona. Problem został rozwiązany poprzez zmianę obrazu bazowego w Dockerfile na minimalistyczną dystrybucję python:3.11-alpine oraz dodanie instrukcji wymuszającej aktualizację bibliotek systemowych (pip, wheel, jaraco.context). Po tym zabiegu skaner wykazał 0 podatności.

### 3. Budowanie Multi-Arch i Publikacja w GHCR
* Po pomyślnym przejściu skanowania, obraz jest budowany jednocześnie dla architektur linux/amd64 (standardowe PC) oraz linux/arm64 (np. procesory Apple Silicon czy Raspberry Pi).
* Gotowy pakiet jest automatycznie wysyłany do oficjalnego rejestru GHCR pod adres: ghcr.io/wikluk-lab/zad2.

---

## Schemat tagowania obrazów

Wdrożono elastyczny system wersjonowania kontenerów. Podczas każdego udanego przejścia potoku, obraz otrzymuje dwa niezależne tagi:

1. **latest** – zawsze wskazuje na najnowszą, aktualną wersję aplikacji w głównym produkcyjnym kodzie.
2. **${{ github.sha }}** – unikalny tag generowany na podstawie skrótu (SHA) konkretnego commitu z Gita. Pozwala to na pełną identyfikowalność.

---

## Potwierdzenie poprawności działania
Łańcuch GitHub Actions został uruchomiony i pomyślnie zweryfikowany. Wszystkie etapy od logowania, przez kompilację środowiska, bezbłędny test Trivy, aż po spakowanie manifestu Multi-Arch i push do GHCR kończą się zielonym statusem powodzenia.
