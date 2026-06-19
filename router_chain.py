from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_client import llm
from datetime import datetime


def get_date_context():
    return datetime.now().strftime("Today is %A, %B %d, %Y.")

router_prompt = PromptTemplate(
    input_variables=["date_context", "message", "chat_history"],
    template="""
        You are a routing system for a chatbot.

        Today's date: {date_context}

        Chat history:
        {chat_history}

        User message and the message that should determine your output: 
        {message}

        Choose ONE:
        - SEARCH: user EXPLICITLY asks to search, look up, or find information
        - NONE: everything else or if you are unsure, even slightly unsure

        UNNECESSARY SEARCH IS STRICTLY PROHIBITED
        Return ONLY one word: SEARCH or NONE
        """
)

rephrase_prompt = PromptTemplate(
    input_variables=["message", "chat_history"],
    template="""
        You are a query rewriting assistant.

        Chat history:
        {chat_history}

        Latest user message:
        {message}

        Rewrite the latest user message into a standalone search query, a simple query to search for in a search engine.

        Rules:

        Resolve pronouns like "it", "that", "they", etc.
        Use relevant context from the conversation.
        Preserve the user's intent.
        Do not answer the question.
        Return only the rewritten query.

        Standalone search query:
        """
    )

rephrase_chain = rephrase_prompt | llm | StrOutputParser()

def rephrase_question(message, chat_history):
    return rephrase_chain.invoke({
    "message": message,
    "chat_history": chat_history
    }).strip()

router_chain = router_prompt | llm | StrOutputParser()

def route_query(message, chat_history):
    result = router_chain.invoke({
        "date_context": get_date_context(),
        "message": message,
        "chat_history": chat_history
    }).strip().upper()

    if result not in ["SEARCH", "NONE"]:
        print('ERROR IN ROUTER OUTPUT GENERATION, OUTPUT = "' + result + '"')
        if "NONE" in result:
            return "NONE"
        elif "SEARCH" in result:
            return "SEARCH"
        return "NONE"
    return result
