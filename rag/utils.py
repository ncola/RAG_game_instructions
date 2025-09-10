def format_docs(docs, max_docs: int = 8) -> str:
    blocks = []
    seen = set()
    for i, doc in enumerate(docs, 1):
        key = (doc.metadata.get("source"), doc.metadata.get("page"))
        if key in seen:
            continue
        seen.add(key)
        src = doc.metadata.get("source", "?")
        page = doc.metadata.get("page")
        head = f"[{i}] {src}" + (f" (s. {page})" if page is not None else "")
        blocks.append(f"{head}\n{doc.page_content}")
        if len(blocks) >= max_docs:
            break
    return "\n\n".join(blocks)

def sources_line(docs) -> str:
    uniq = []
    for doc in docs:
        src = doc.metadata.get("source", "?")
        page = doc.metadata.get("page")
        tag = f"{src}" + (f", s. {page}" if page is not None else "")
        if tag not in uniq:
            uniq.append(tag)
    return "Źródła: " + "; ".join(uniq)

def build_messages(system_prompt:str, history, question:str, context_block:str):

    msgs = []
    msgs.append({"role": "system", "content": system_prompt})

    trimmed = history[-6:] if history else []
    for role, content in trimmed:
        msgs.append({"role": role, "content": content})

    user_msg = (
        f"PYTANIE:\n{question}\n\n"
        f"KONTEKST (fragmenty instrukcji – odpowiadaj wyłącznie na jego podstawie):\n"
        f"{context_block}\n\n"
        "Jeśli brakuje informacji w kontekście, powiedz to wprost."
    )
    msgs.append({"role": "user", "content": user_msg})
    return msgs
