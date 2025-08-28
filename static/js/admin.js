document.addEventListener('DOMContentLoaded', () => {
    const fetchBtn = document.getElementById('fetch-btn');
    const youtubeUrlInput = document.getElementById('youtube-url');
    const ytIdInput = document.getElementById('yt_id');
    const titleInput = document.getElementById('title');
    const descriptionInput = document.getElementById('description');
    const statusMessage = document.getElementById('status-message');

    fetchBtn.addEventListener('click', () => {
        const url = youtubeUrlInput.value;
        if (!url) {
            statusMessage.textContent = 'Вставте посилання!';
            return;
        }

        const videoIdMatch = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?.*v=|embed\/|v\/|shorts\/))([^?&\n]+)/);
        if (!videoIdMatch || videoIdMatch.length < 2) {
            statusMessage.textContent = 'Неправильне посилання на YouTube.';
            return;
        }
        const videoId = videoIdMatch[1];
        
        statusMessage.textContent = 'Отримання даних...';
        ytIdInput.value = videoId;

        fetch(`/api/get_video_info?yt_id=${videoId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                titleInput.value = data.title || '';
                descriptionInput.value = data.description || '';
                statusMessage.textContent = 'Дані успішно отримано!';
            })
            .catch(error => {
                console.error('Помилка отримання даних:', error);
                statusMessage.textContent = 'Помилка отримання даних. Спробуйте вручну.';
            });
    });
});