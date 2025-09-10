# 🎲 Game Instructions RAG 🎲
System RAG (Retrieval-Augmented Generation), który ma wgrane instrukcje gier planszowych w formacie PDF i potrafi odpowiadać na pytania dotyczące zasad.
Bot wyszukuje fragmenty instrukcji, przekazuje je jako kontekst do modelu LLM i zwraca odpowiedź wraz z podaniem źródeł.

## Stack technologiczny 
- Python 3.10+
- LangChain – obsługa pipeline’u RAG
- ChromaDB – wektorowa baza danych (embeddingi instrukcji)
- PyMuPDF – parser PDF
- OpenAI GPT – model językowy do generowania odpowiedzi
- Streamlit – prosty UI chatu
- python-dotenv – obsługa klucza API z .env

## Architektura 
data/ – przechowuje instrukcje gier (PDF)
index/ – moduł indeksowania: ładuje dokumenty, dzieli je na fragmenty, tworzy embeddingi i zapisuje je w bazie wektorowej (ChromaDB) lub ją aktualizuje
rag/ – moduł RAG: pobiera fragmenty z bazy, buduje prompty i wysyła je do modelu LLM, zwraca odpowiedzi wraz ze źródłami
models/ – konfiguracje bota i modelu (np. parametry retrievera, temperatury)
config.py – ustawienia projektu i treści promptów systemowych
app.py – aplikacja Streamlit z prostym interfejsem czatu
chroma_db/ – trwała baza embeddingów

## Przykładowe pytania
"Jak liczyć punkty w Carcassonne?”
"O co chodzi w Dobble?”

## Funkcje
- Wczytuje instrukcje gier z plików PDF i buduje bazę wektorową (ChromaDB)
- Wyszukuje odpowiednie fragmenty dokumentów i podaje je jako kontekst dla LLM
- Odpowiada tylko na podstawie kontekstu
- Wyświetla źródła (plik i strona)
- Streamlit UI – prosty chat z botem
- Obsługa API key z .env albo możliwość wpisania klucza ręcznie w aplikacji

## Najblizsze TODO 
- czyszczenie tekstu przed chunkowaniem oraz lepsze metadane
- streaming tokenów (odpowiedzi na żywo)
- lepsze zarządzanie historią 
- dockerfile do łatwego uruchamiania

## Źródła 
instrukcje pochodzą ze strony:
https://am76.pl/instrukcje?srsltid=AfmBOoqPdCfI1B1s_IpLrwl5PPjqR_DJzzGkIMQBWdKWXg6-7R7CLBCG

