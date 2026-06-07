# Zadanie 2 – Potok CI/CD w GitHub Actions

Repozytorium zawiera realizację potoku CI/CD przy użyciu GitHub Actions dla aplikacji pogodowej z Zadania 1. Potok automatyzuje proces budowania, skanowania pod kątem bezpieczeństwa oraz publikacji obrazu kontenera.

## Struktura projektu
* `.github/workflows/ci-cd.yml` – definicja potoku GitHub Actions.
* `Dockerfile` – konfiguracja wieloetapowego budowania obrazu (Multi-stage build) opartego na bezpiecznym obrazie `python:3.11-alpine`.
* `requirements.txt` – plik zależności aplikacji Python.
* `main.py` – kod źródłowy aplikacji.

---

## Opis konfiguracji i realizacji etapów zadania

### 1. Budowanie i mechanizm pamięci podręcznej (Cache)
W etapie budowania wykorzystano akcję `docker/build-push-action@v6`. W celu optymalizacji czasu działania potoku wdrożono zewnętrzny mechanizm pamięci podręcznej (cache) przechowywany w rejestrze Docker Hub pod adresem `docker.io/wikluks2/app-cache:cache`. Warstwy obrazu są pobierane i zapisywane z parametrem `mode=max`, co znacznie skraca czas kolejnych uruchomień potoku.

### 2. Testy bezpieczeństwa (Skanowanie CVE)
Zgodnie z wymaganiami bezpieczeństwa, przed publikacją obrazu uruchamiane jest automatyczne skanowanie podatności za pomocą narzędzia **Trivy** (`aquasecurity/trivy-action@v0.24.0`). 
* Skaner weryfikuje obecność luk o statusie **HIGH** oraz **CRITICAL**.
* Konfiguracja zawiera warunek błędu (`exit-code: '1'`), co oznacza, że wykrycie jakiejkolwiek poważnej luki bezpieczeństwa natychmiast przerywa i blokuje dalsze kroki potoku (obraz nie zostanie opublikowany).
* W celu zapewnienia pełnego bezpieczeństwa, obraz bazowy został zoptymalizowany do wersji `alpine`, a fabryczne pakiety Pythona są aktualizowane wewnątrz `Dockerfile`, co pozwoliło uzyskać wynik 0 podatności systemowych.

### 3. Budowanie wieloarchitekturowe (Multi-Arch)
Po pomyślnym przejściu testów bezpieczeństwa, potok buduje ostateczną wersję obrazu jednocześnie dla dwóch architektur sprzętowych:
* `linux/amd64`
* `linux/arm64`

Wykorzystano do tego emulator `QEMU` (`docker/setup-qemu-action@v3`) oraz `Docker Buildx` (`docker/setup-buildx-action@v3`).

### 4. Publikacja w rejestrze GHCR
Gotowy, bezpieczny obraz wieloarchitekturowy jest automatycznie wypychany do rejestru **GitHub Container Registry (GHCR)** na konto organizacji/użytkownika: `ghcr.io/wikluk-lab/zad2`.

---

## Schemat tagowania obrazów

Wdrożono elastyczny i powszechnie stosowany w branży schemat wersjonowania (tagowania) obrazów kontenerów. Każdy zbudowany kontener otrzymuje jednocześnie dwa tagi:

1. `latest` – tag wskazujący na najnowszą, aktualnie zbudowaną wersję obrazu w gałęzi głównej. Przydatny do pobierania zawsze aktualnej wersji.
2. `${{ github.sha }}` – unikalny tag odpowiadający pełnemu identyfikatorowi (SHA) commitu z GitHuba, który wywołał potok. Zapewnia to pełną identyfikowalność – dokładnie wiadomo, z której wersji kodu źródłowego powstał dany kontener, i pozwala na łatwy powrót (rollback) do starszych wersji.

```yaml
tags: |
  ghcr.io/wikluk-lab/zad2:latest
  ghcr.io/wikluk-lab/zad2:${{ github.sha }}
