from router_chain import route_query, rephrase_question
from rag_chain import answer_with_context
from chat_memory import format_history
from llm_client import llm
from config_loader import load_config
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime


def get_date_context():
    return datetime.now().strftime("Today is %A, %B %d, %Y.")

general_prompt = PromptTemplate(
    input_variables=["mission", "rules", "current_date", "chat_history", "question"],
    template="""
            Your mission:
            {mission}

            Rules:
            {rules}

            Current date:
            {current_date}

            Chat history:
            {chat_history}

            User prompt:
            {question}

            Reply naturally. Do not mention internal steps or reasoning.
            """
)

general_chain = general_prompt | llm | StrOutputParser()


def process_message(message, history):
    chat_history = format_history(history)
    action = route_query(message, chat_history)
    mission, rules = load_config()

    db_sources = []
    web_sources = []
    response = ""

    if action == "SEARCH":
        search_query = rephrase_question(message, chat_history)

        response, db_sources, web_results = answer_with_context(
            mission,
            rules,
            message,
            chat_history,
            search_query
        )

        web_sources = [
            r.get("url")
            for r in web_results
            if r.get("url")
        ]

    else:
        response = general_chain.invoke({
            "mission": mission,
            "rules": rules,
            "current_date": get_date_context(),
            "chat_history": chat_history,
            "question": message
        })

    history.add_user_message(message)
    history.add_ai_message(response)

    return {
        "response": response,
        "chat_history": chat_history,
        "action": action,
        "db_sources": db_sources,
        "web_sources": web_sources
    }