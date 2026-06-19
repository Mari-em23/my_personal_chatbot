from flask import render_template, request, session
from chat_memory import get_json_history, format_history
def init_routes(app):
    @app.route('/')
    def chatbot():
        return render_template("index.html")

    from Flask.services.chat_service import process_message
    from chat_memory import get_history

    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.json
        message = data.get('message', '').strip()
        if not message:
            return {"error": "Empty message"}, 400
        
        session_id = session.get("session_id")
        history = get_history(session_id)

        try:
            result = process_message(message, history)
            return result
        except Exception as e:
            print(f"[ERROR] Chat failed: {e}")
            return {"error": str(e)}, 500
        
    @app.route('/api/history', methods=['GET'])
    def chat_history():
        session_id = session.get("session_id")
        chat_history = get_json_history(session_id)
        return chat_history