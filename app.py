import streamlit as st

from rag.bot import Bot
from models.models import BotConfig, LLMConfig

import time

from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    st.set_page_config(page_title="RuleMaster – AI Assistant for Board Game Rules", page_icon="🎲")
    st.title("🎲 RuleMaster – AI Assistant for Board Game Rules")

    with st.sidebar:
        st.header("Settings")
        env_key = os.getenv("OPENAI_API_KEY", "")
        options = []
        if env_key:
            options.append(f"Use from .env")
        options.append("Enter manually")

        choice = st.radio("API key source", options, index=0 if env_key else 1)

        if "api_key" not in st.session_state:
            st.session_state.api_key = None

        if choice.startswith("Use from .env"):
            st.session_state.api_key = None
            st.caption("The key will be loaded from the environment variable `OPENAI_API_KEY`.")
        else:
            ui_key = st.text_input("Enter the key (sk-…)", type="password")
            if st.button("Use this key"):
                if ui_key and ui_key.startswith("sk-"):
                    st.session_state.api_key = ui_key
                    st.success(f"✅ Key set for this session)")
                else:
                    st.error("❌ Looks like an invalid key (must start with `sk-`).")
    
        score_threshold = st.slider("Minimum document matching level",0.0, 1.0, 0.75)

    bot_cfg = BotConfig(score_threshold=score_threshold,)
    llm_cfg = LLMConfig()

    bot = Bot(bot_cfg, api_key=st.session_state.api_key)

    if "history" not in st.session_state:
            st.session_state.history = []

    # display chat messages from history on app rerun
    for role, content in st.session_state.history:
        with st.chat_message(role):
            st.markdown(content)

    if user_input:= st.chat_input("Ask question about board game"):
        #question
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.history.append(("user", user_input))
        
        #answer
        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("Thinking..."):
                time.sleep(0.3)
                answer, sources = bot.answer(user_input, history=st.session_state.history)
            placeholder.markdown(f"{answer}\n\n{sources}")
            
        st.session_state.history.append(("assistant", f"{answer}\n\n{sources}"))

if __name__ == "__main__":
    main()