from datetime import datetime

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_client import llm
from semantic_search import search_with_details
from web_search import search_and_crawl, build_web_context

def get_date_context():
    return datetime.now().strftime("Today is %A, %B %d, %Y.")

def retrieve_db_context(query, top_k=5):
    results = search_with_details(query, top_k=top_k)

    if not results:
        return "", []

    parts = []

    for r in results:
        parts.append(r["passage"])  

    return "\n---\n".join(parts), results

prompt = PromptTemplate(
    input_variables=[
        "mission",
        "rules",
        "date_context",
        "db_context",
        "web_context",
        "chat_history",
        "question",
        "search_query"
    ],
    template="""
        Current date : {date_context}

        === YOUR MISSION ===
        {mission}

        === RULES ===
        {rules}

        === INTERNAL DATABASE ===
        {db_context}

        === WEB DATA ===
        {web_context}

        === ORIGINAL USER QUESTION (what you should actually answer !!) ===
        {question}

        == RSEARCH QUERY ==
        {search_query}

        This is the chat history for more context :
        {chat_history}

        Instructions:
        - Synthesize information from internal DB, web sources, chat history and the user question
        - If you judged an information irrelevant, just do not mention it in your answer
        - Prioritize internal DB
        - Use web sources for broader context
        - Indicate whether information comes from internal DB or web
        - If no relevant information is found, say so clearly
        - Be natural and conversational
        - Keep in mind the difference between what the actual user prompt and the rephrased question used as search query
        - Keep in mind that your main task is to answer the user's prompt, the user doesnt need to know about any reasoning you did to provide the answer
        - No greeting neeeded, only answer the question
        """
)

rag_chain = prompt | llm | StrOutputParser()

def answer_with_context(mission, rules, question, chat_history, search_query):
    db_context, db_sources = retrieve_db_context(search_query)
    web_results = search_and_crawl(search_query, max_results=5)
    web_context = build_web_context(web_results)

    if not db_context:
        db_context = "No relevant internal data found."
    if not web_context:
        web_context = "No relevant web results found."

    response = rag_chain.invoke({
        "mission": mission,
        "rules": rules,
        "date_context": get_date_context(),
        "db_context": db_context,
        "web_context": web_context,
        "chat_history": chat_history,
        "question": question,
        "search_query": search_query
    })

    return response, db_sources, web_results