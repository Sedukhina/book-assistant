import { setAnimation } from './3dModel.js';


document.getElementById('recordButton').addEventListener('click', async () => {
    const chatContainer = document.getElementById('chatContainer');

    // Change animation to "Spin" when recording starts
    setAnimation('Spin');

    const recordingMessage = document.createElement('div');
    recordingMessage.className = 'message assistant-message';
    recordingMessage.innerText = 'Запис...';
    chatContainer.appendChild(recordingMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        const response = await fetch('/chat/record'); // Оновлений шлях
        const data = await response.json();

        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.innerText = data.text;
        chatContainer.appendChild(userMessage);

        const assistantMessage = document.createElement('div');
        assistantMessage.className = 'message assistant-message';
        assistantMessage.innerText = data.response;
        chatContainer.appendChild(assistantMessage);

        if (data.audio_file) {
            const audio = document.createElement('audio');
            audio.className = 'audio-response';
            audio.controls = true;
            audio.src = `${data.audio_file}?t=${new Date().getTime()}`;
            assistantMessage.appendChild(audio);

            // Change animation to "Eat" while audio is playing
            audio.play();
            setAnimation('Eat');

            // When audio ends, return to idle animation
            audio.addEventListener('ended', () => {
                setAnimation('Idle_A');
            });
        } else {
            // If no audio file is returned, revert to idle
            setAnimation('Idle_A');
        }

        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (error) {
        console.error('Помилка:', error);

        const errorMessage = document.createElement('div');
        errorMessage.className = 'message assistant-message';
        errorMessage.innerText = 'Помилка запису або розпізнавання.';
        chatContainer.appendChild(errorMessage);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Revert animation to idle in case of error
        setAnimation('Idle_A');
    }
});


document.getElementById('sendButton').addEventListener('click', async () => {
    const chatContainer = document.getElementById('chatContainer');
    const chatInput = document.getElementById('chatInput');
    const userMessage = chatInput.value.trim(); // Отримуємо текст із поля введення

    if (!userMessage) return; // Якщо поле порожнє, нічого не робимо

    // Додаємо повідомлення користувача у чат
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message user-message';
    userMessageElement.innerText = userMessage;
    chatContainer.appendChild(userMessageElement);
    chatInput.value = ''; // Очищуємо поле введення
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        // Надсилаємо текст на сервер
        const response = await fetch('/chat/manual', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: userMessage }),
        });

        const data = await response.json();

        // Додаємо відповідь асистента
        const assistantMessageElement = document.createElement('div');
        assistantMessageElement.className = 'message assistant-message';
        assistantMessageElement.innerText = data.response;
        chatContainer.appendChild(assistantMessageElement);

        // Відтворюємо аудіо, якщо доступне
        if (data.audio_file) {
            const audio = document.createElement('audio');
            audio.className = 'audio-response';
            audio.controls = true;
            audio.src = `${data.audio_file}?t=${new Date().getTime()}`;
            assistantMessageElement.appendChild(audio);

            // Анімація "говоріння" під час відтворення
            audio.play();
            setAnimation('Eat');

            // Повернення до "Idle" після закінчення відтворення
            audio.addEventListener('ended', () => {
                setAnimation('Idle_A');
            });
        }

        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (error) {
        console.error('Помилка:', error);

        const errorMessageElement = document.createElement('div');
        errorMessageElement.className = 'message assistant-message';
        errorMessageElement.innerText = 'Сталася помилка при обробці вашого запиту.';
        chatContainer.appendChild(errorMessageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});

document.getElementById('sendButton').addEventListener('click', async () => {
    const chatInput = document.getElementById('chatInput');
    const userMessage = chatInput.value.trim();

    if (!userMessage) return;

    // Додаємо повідомлення користувача в чат
    addMessageToChat(userMessage, 'user-message');
    chatInput.value = '';

    try {
        const response = await fetch('/api/gpt-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: userMessage }),
        });

        const data = await response.json();
        addMessageToChat(data.response, 'assistant-message');
    } catch (error) {
        console.error('Помилка:', error);
        addMessageToChat('Сталася помилка при обробці вашого запиту.', 'assistant-message');
    }
});


// function addRecommendationsToChat(recommendations) {
//     const chatContainer = document.getElementById('chatContainer');
//     const messageElement = document.createElement('div');
//     messageElement.className = 'message assistant-message';

//     let recommendationHTML = '<strong>Book Recommendations:</strong><ul>';
//     recommendations.forEach(book => {
//         recommendationHTML += `
//             <li>
//                 <strong>${book.title}</strong> by ${book.author}<br>
//                 <em>${book.description}</em><br>
//                 <strong>Published:</strong> ${book.published}<br>
//                 <strong>Categories:</strong> ${book.categories.join(', ')}<br>
//                 <strong>ISBN:</strong> ${book.isbn}
//             </li>
//         `;
//     });
//     recommendationHTML += '</ul>';

//     messageElement.innerHTML = recommendationHTML;
//     chatContainer.appendChild(messageElement);
//     chatContainer.scrollTop = chatContainer.scrollHeight;
// }

