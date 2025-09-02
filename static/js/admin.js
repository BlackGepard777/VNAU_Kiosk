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

document.addEventListener('DOMContentLoaded', () => {
    const idleFetchBtn = document.getElementById('idle-fetch-btn');
    const idleYoutubeUrlInput = document.getElementById('idle-youtube-url');
    const idleYtIdInput = document.getElementById('idle-yt_id');
    const idleTitleInput = document.getElementById('idle-title');
    const idleStatusMessage = document.getElementById('idle-status-message');
    const addIdleVideoForm = document.getElementById('add-idle-video-form');

    idleFetchBtn.addEventListener('click', () => {
        const url = idleYoutubeUrlInput.value;
        if (!url) {
            idleStatusMessage.textContent = 'Вставте посилання!';
            return;
        }

        const videoIdMatch = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?.*v=|embed\/|v\/|shorts\/))([^?&\n]+)/);
        if (!videoIdMatch || videoIdMatch.length < 2) {
            idleStatusMessage.textContent = 'Неправильне посилання на YouTube.';
            return;
        }
        const videoId = videoIdMatch[1];

        idleStatusMessage.textContent = 'Отримання даних...';
        idleYtIdInput.value = videoId;

        fetch(`/api/get_video_info?yt_id=${videoId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) throw new Error(data.error);
                idleTitleInput.value = data.title || '';
                idleStatusMessage.textContent = 'Дані успішно отримано!';
            })
            .catch(error => {
                console.error('Помилка отримання даних:', error);
                idleStatusMessage.textContent = 'Помилка отримання даних. Спробуйте вручну.';
            });
    });

    addIdleVideoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addIdleVideoForm);
        await fetch('/admin/idle/add', {
            method: 'POST',
            body: new URLSearchParams(formData)
        });
        location.reload(); 
    });

    document.querySelectorAll('.idle-toggle').forEach(checkbox => {
        checkbox.addEventListener('change', async (e) => {
            const videoId = e.target.dataset.id;
            const isChecked = e.target.checked;
            await fetch('/admin/idle/toggle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_id: videoId, is_active: isChecked })
            });
            location.reload();
        });
    });

    document.querySelectorAll('.delete-idle-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            const videoId = e.target.dataset.id;
            await fetch('/admin/idle/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_id: videoId })
            });
            location.reload();
        });
    });
});