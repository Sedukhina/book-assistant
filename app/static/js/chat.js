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
