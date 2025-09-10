import streamlit as st

from rag.bot import Bot
from models.models import BotConfig, LLMConfig

from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    st.set_page_config(page_title="RAG Bot – instrukcje gier", page_icon="🎲")
    st.title("🎲 RAG Bot – instrukcje gier")

    with st.sidebar:
        st.header("Ustawienia")
        env_key = os.getenv("OPENAI_API_KEY", "")
        options = []
        if env_key:
            options.append(f"Użyj z .env")
        options.append("Podaj ręcznie")

        choice = st.radio("Źródło klucza API", options, index=0 if env_key else 1)

        if "api_key" not in st.session_state:
            st.session_state.api_key = None

        if choice.startswith("Użyj z .env"):
            st.session_state.api_key = None
            st.caption("Klucz będzie wczytany z zmiennej środowiskowej `OPENAI_API_KEY`.")
        else:
            ui_key = st.text_input("Wpisz klucz (sk-…)", type="password")
            if st.button("Użyj tego klucza"):
                if ui_key and ui_key.startswith("sk-"):
                    st.session_state.api_key = ui_key
                    st.success(f"✅ Klucz ustawiony na czas tej sesji)")
                else:
                    st.error("❌ Wygląda na nieprawidłowy klucz (musi zaczynać się od `sk-`).")
    
        score_threshold = st.slider("Minimalny poziom dopasowania dokumentu",0.0, 1.0, 0.75)

    bot_cfg = BotConfig(score_threshold=score_threshold,)
    llm_cfg = LLMConfig()

    bot = Bot(bot_cfg, api_key=st.session_state.api_key)

    if "history" not in st.session_state:
            st.session_state.history = []

    user_input = st.chat_input("Zadaj pytanie")
    if user_input:

        answer, sources = bot.answer(user_input, history=st.session_state.history)

        st.session_state.history.append(("user", user_input))
        st.session_state.history.append(("assistant", f"{answer}\n\n{sources}"))

        for role, content in st.session_state.history:
            with st.chat_message(role):
                st.markdown(content)


if __name__ == "__main__":
    main()