document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    // --- FastAPI Backend URL ---
    const apiUrl = 'http://127.0.0.1:8000/api/v1/ask';

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInput.value.trim();
        if (!question) return;

        appendMessage('user', question);
        userInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question, language: 'Polish' }),
            });

            removeTypingIndicator();

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Błąd serwera');
            }

            const data = await response.json();
            appendMessage('bot', data.answer, data.sources);
        } catch (error) {
            removeTypingIndicator();
            appendMessage('bot', `Przepraszam, wystąpił błąd: ${error.message}`);
        }
    });

    function appendMessage(sender, text, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        const textP = document.createElement('p');
        textP.textContent = text;
        messageDiv.appendChild(textP);

        if (sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.classList.add('sources');

            const sourcesTitle = document.createElement('p');
            sourcesTitle.textContent = 'Źródła:';
            sourcesDiv.appendChild(sourcesTitle);

            sources.forEach(source => {
                const sourceLink = document.createElement('a');
                sourceLink.href = source.url;
                sourceLink.textContent = source.title || source.url;
                sourceLink.target = '_blank';
                sourcesDiv.appendChild(sourceLink);
                sourcesDiv.appendChild(document.createElement('br'));
            });
            messageDiv.appendChild(sourcesDiv);
        }

        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.classList.add('message', 'bot-message', 'typing-indicator');
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `<span></span><span></span><span></span>`;
        chatWindow.appendChild(indicator);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
});