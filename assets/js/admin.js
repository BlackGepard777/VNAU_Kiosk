document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('videos-form');
    const videosList = document.getElementById('videos-list');

    function renderVideos() {
        fetch('/api/videos')
            .then(response => response.json())
            .then(videos => {
                videosList.innerHTML = '<h2>Наявні відео</h2>';
                videos.forEach(video => {
                    const videoItem = document.createElement('div');
                    videoItem.classList.add('list-item');
                    videoItem.innerHTML = `
                        <div class="item-details">
                            <h3>${video.title}</h3>
                            <p>ID: ${video.youtube_id}</p>
                            <p>Категорія: ${video.category}</p>
                        </div>
                        <div class="item-actions">
                            <button onclick="deleteVideo(${video.id})">Видалити</button>
                        </div>
                    `;
                    videosList.appendChild(videoItem);
                });
            });
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const youtubeId = document.getElementById('video-id').value;
        const title = document.getElementById('video-title').value;
        const description = document.getElementById('video-description').value;
        const category = document.getElementById('video-category').value; // Отримуємо значення категорії

        fetch('/api/videos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ youtube_id: youtubeId, title, description, category }) // Відправляємо категорію на сервер
        })
        .then(() => {
            form.reset();
            renderVideos();
        });
    });

    window.deleteVideo = (id) => {
        if (confirm('Ви впевнені?')) {
            fetch(`/api/videos/${id}`, { method: 'DELETE' }).then(() => renderVideos());
        }
    };

    renderVideos();
});