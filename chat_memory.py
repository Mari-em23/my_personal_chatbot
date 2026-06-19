from langchain_core.chat_history import InMemoryChatMessageHistory

# One history object per user session
session_histories = {}
def get_history(user_id):
    if user_id not in session_histories:
        session_histories[user_id] = InMemoryChatMessageHistory()
    return session_histories[user_id]

def format_history(history):
    messages = history.messages[-60:] # 1 user message + 1 AI response = 1 exchange so last 6 exchanges
    if not messages:
        return ""
    lines = []
    for m in messages:
        role = "User" if m.type == "human" else "Assistant"
        lines.append(f"{role} : {m.content}")
    return "\n".join(lines)

def get_json_history(user_id):
    history = session_histories.get(user_id)
    if not history:
        return []

    messages = history.messages[-60:]

    result = []
    for m in messages:
        role = "user" if m.type == "human" else "assistant"
        result.append({
            "role": role,
            "content": m.content
        })
    return result