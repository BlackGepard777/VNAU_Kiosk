// Функція для ініціалізації сторінки з відео
const initVideosPage = () => {
    const videoGrid = document.getElementById('video-grid');
    if (!videoGrid) {
        console.error('Елемент з id "video-grid" не знайдено.');
        return;
    }
    
    // Виконуємо запит до нашого Flask API
    fetch('/api/videos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Помилка завантаження API');
            }
            return response.json();
        })
        .then(videos => {
            videoGrid.innerHTML = '';

            if (videos.length === 0) {
                videoGrid.innerHTML = `<p style="text-align: center; color: #666;">Наразі відео відсутні. Додайте їх через адмін-панель.</p>`;
                return;
            }
            
            videos.forEach(video => {
                const videoCard = document.createElement('div');
                videoCard.classList.add('video-card');

                videoCard.innerHTML = `
                    <iframe 
                        width="100%" 
                        height="250"
                        src="https://www.youtube.com/embed/${video.youtube_id}" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                    <div class="video-info">
                        <h3 class="video-title">${video.title}</h3>
                        <p class="video-description">${video.description || ''}</p>
                    </div>
                `;
                videoGrid.appendChild(videoCard);
            });
        })
        .catch(error => {
            console.error('Помилка завантаження відео:', error);
            videoGrid.innerHTML = `<p style="text-align: center; color: red;">Не вдалося завантажити відео.</p>`;
        });
};