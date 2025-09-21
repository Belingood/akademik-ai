# AkademikAI 🎓

[![Licencja: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Wersja Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Framework AI: LangChain](https://img.shields.io/badge/AI-LangChain-purple.svg)](https://www.langchain.com/)

AkademikAI to API oparte na architekturze RAG (Retrieval-Augmented Generation), zaprojektowane jako inteligentny asystent informacyjny dla uczelni wyższej. System wykorzystuje wektorową bazę danych, zasilaną treściami z oficjalnej strony internetowej uczelni, aby udzielać precyzyjnych, opartych na kontekście odpowiedzi na pytania użytkowników.

---

## ✨ Funkcjonalności

-   **Inteligentne Pytania i Odpowiedzi**: Zadawaj złożone pytania w języku naturalnym i otrzymuj zwięzłe, rzeczowe odpowiedzi.
-   **Weryfikacja Źródeł**: Każda odpowiedź jest poparta linkami do oryginalnych stron internetowych, co zapewnia transparentność i wiarygodność.
-   **Wsparcie dla Wielu Języków**: API potrafi generować odpowiedzi w różnych językach (np. polskim, angielskim) na podstawie prostego parametru.
-   **Szybkość i Skalowalność**: Zbudowany przy użyciu FastAPI dla wysokiej wydajności, napędzany przez najnowocześniejsze modele językowe i wyszukiwanie wektorowe.
-   **Łatwa Konfiguracja**: Projekt zawiera jasne instrukcje dotyczące lokalnej instalacji oraz opcję akceleracji GPU do budowy bazy wiedzy.

---

## 🛠️ Stos Technologiczny

-   **Backend**: FastAPI
-   **Orkiestracja AI**: LangChain
-   **LLM**: GPT-4o (przez API OpenAI)
-   **Wektorowa Baza Danych**: ChromaDB
-   **Model Embeddingów**: `intfloat/multilingual-e5-large`
-   **Konfiguracja**: Pydantic

---

## 🚀 Pierwsze Kroki

Postępuj zgodnie z poniższymi instrukcjami, aby skonfigurować i uruchomić projekt lokalnie.

### 1. Wymagania Wstępne

-   Python 3.9+
-   Git

### 2. Klonowanie Repozytorium

```bash
git clone https://github.com/twoja-nazwa-uzytkownika/akademik-ai.git
cd akademik-ai
```

### 3. Konfiguracja Środowiska

Utwórz i aktywuj środowisko wirtualne:

```bash
# Dla systemów macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Dla systemu Windows
python -m venv venv
.\venv\Scripts\activate
```

Zainstaluj wymagane pakiety Python:

```bash
pip install -r requirements.txt
```

### 4. Konfiguracja Zmiennych Środowiskowych

Aplikacja wymaga klucza API od OpenAI.

1.  Skopiuj przykładowy plik środowiskowy:
    ```bash
    # Dla macOS/Linux
    cp .env.example .env

    # Dla Windows
    copy .env.example .env
    ```
2.  Otwórz nowo utworzony plik `.env` i dodaj swój klucz API OpenAI:
    ```
    OPENAI_API_KEY="sk-TutajWklejSwójSekretnyKlucz"
    ```

### 5. Budowanie Bazy Wiedzy (Indeksacja)

Aby odpowiadać na pytania, system potrzebuje przetworzonej bazy wiedzy. Proces ten nazywa się indeksacją. Możesz go przeprowadzić na dwa sposoby:

#### Opcja A: Lokalnie na CPU (prosta, ale bardzo wolna)

Ta metoda jest odpowiednia dla małych zbiorów danych lub do szybkich testów. Dla pełnego zbioru danych proces może zająć wiele godzin na standardowym procesorze.

-   Upewnij się, że plik z danymi znajduje się w `data/content.jsonl`.
-   Uruchom skrypt indeksujący z terminala:
    ```bash
    python scripts/build_index.py
    ```
    Baza danych zostanie utworzona w folderze `vector_db/`.

#### Opcja B: Akceleracja GPU w Chmurze (zalecana, szybka)

Ta metoda wykorzystuje darmowe lub płatne zasoby Google Colab i jest **znacznie szybsza** (1-2 godziny zamiast kilkunastu). Jest to zalecany sposób dla dużych zbiorów danych.

1.  Przejdź do folderu `colab_notebooks/`.
2.  Otwórz plik `AkademikAI_Indexing_GPU.ipynb` w Google Colab.
3.  Postępuj zgodnie z instrukcjami w notatniku, aby załadować dane, przeprowadzić indeksację i pobrać gotową bazę danych w formie archiwum `.zip`.
4.  Rozpakuj archiwum i umieść folder `vector_db` w głównym katalogu tego projektu.

### 6. Uruchomienie Serwera API

Gdy folder `vector_db` jest gotowy, uruchom serwer FastAPI:

```bash
uvicorn src.main:app --reload
```

API będzie działać pod adresem `http://127.0.0.1:8000`.

### 7. Uruchomienie Demonstracyjnego Czat-Interfejsu (Opcjonalnie)

Aby zwizualizować działanie API, możesz uruchomić prostą aplikację webową z interfejsem czatu, opartą na Flask. Wymaga to uruchomienia dwóch terminali jednocześnie.

-   **Terminal 1 (Uruchomienie Backendu FastAPI):**
    Jeśli serwer API jeszcze nie działa, uruchom go:
    ```bash
    uvicorn src.main:app --reload
    ```

-   **Terminal 2 (Uruchomienie Frontendu Flask):**
    Otwórz nowy terminal i uruchom serwer aplikacji demonstracyjnej:
    ```bash
    python frontend_demo/app.py
    ```

-   **Otwórz Czat:**
    W przeglądarce internetowej przejdź pod adres **[http://127.0.0.1:5000](http://127.0.0.1:5000)**. Możesz teraz rozmawiać z asystentem AkademikAI.

### 8. Eksploracja API

Jeśli chcesz komunikować się z API bezpośrednio, otwórz przeglądarkę internetową i przejdź pod adres **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**, aby uzyskać dostęp do interaktywnej dokumentacji Swagger UI. Możesz przetestować endpoint `/api/v1/ask` bezpośrednio stamtąd.

---

## 📜 Licencja

Ten projekt jest udostępniany na licencji MIT. Zobacz plik [LICENSE](LICENSE), aby uzyskać więcej informacji.