let chatHistory = [];
let chatOpen = true;

window.onload = async function () {
    try {
        const response = await fetch('/api/history', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        console.log(data)
        fetch_chat_history(data || []);
    } catch (err) {
        console.log("No history loaded:", err);
    }
};

function fetch_chat_history(chat_history) {
    for (const message of chat_history) {
        appendMessage(message.role, message.content);
        chatHistory.push(message);
    }
}

function appendMessage(role, content) {
    const messages = document.getElementById('chat-messages');
    const div = document.createElement('div');

    div.className = `mb-2 ${role === 'user' ? 'text-end' : 'text-start'}`;

    div.innerHTML = `
        <span class="badge ${
            role === 'user'
                ? 'bg-primary'
                : 'bg-dark border border-secondary'
        } text-wrap text-start p-2"
        style="max-width:85%; white-space:pre-wrap;">
            ${content}
        </span>
    `;

    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';

    appendMessage('user', message);
    chatHistory.push({ role: 'user', content: message });

    appendMessage('assistant', '...');

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                history: chatHistory.slice(-60)
            })
        });

        const data = await response.json();

        const messages = document.getElementById('chat-messages');
        messages.removeChild(messages.lastChild);

        appendMessage('assistant', data.response);
        chatHistory.push({ role: 'assistant', content: data.response });

    } catch (error) {
        const messages = document.getElementById('chat-messages');
        messages.removeChild(messages.lastChild);
        appendMessage('assistant', 'Error connecting to assistant.');
    }
}