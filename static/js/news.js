document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');
    const announcementsContainer = document.getElementById('announcements-container');

    if (!newsContainer || !announcementsContainer) {
        console.error('Один з контейнерів не знайдено.');
        return;
    }

    const loadAndRenderContent = async (endpoint, container, type) => {
        try {
            const response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error(`Не вдалося завантажити дані з ${endpoint}.`);
            }
            const data = await response.json();

            container.innerHTML = '';
            if (data.length === 0) {
                container.innerHTML = `<p class="no-content">Наразі контенту немає.</p>`;
                return;
            }

            data.forEach(item => {
                const card = document.createElement('div');
                card.classList.add('news-card');

                card.innerHTML = `
                    ${item.image ? `<img src="${item.image}" alt="${item.title}" style="max-width:200px; display:block; margin-bottom:10px;">` : ""}
                    <h3>${item.title}</h3>
                    <p>${item.content}</p>
                    <button class="btn btn-primary btn-sm" data-url="${item.link}" data-type="${type}">Читати далі &rarr;</button>
                `;
                container.appendChild(card);
            });

            container.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('click', () => {
                    const url = btn.getAttribute('data-url');
                    const itemType = btn.getAttribute('data-type');
                    loadItemDetail(url, itemType);
                });
            });

        } catch (error) {
            console.error(`Помилка завантаження даних: ${error}`);
            container.innerHTML = `<p class="error-content">Не вдалося завантажити контент.</p>`;
        }
    };

    // Завантаження новин
    loadAndRenderContent('/api/news', newsContainer, 'news');

    // Завантаження оголошень
    loadAndRenderContent('/api/announcements', announcementsContainer, 'announcement');

    function loadItemDetail(url, type) {
    let endpoint = '';
    if (type === 'news') {
        endpoint = `/api/news/detail?url=${encodeURIComponent(url)}`;
    } else if (type === 'announcement') {
        endpoint = `/api/announcements/detail?url=${encodeURIComponent(url)}`; // правильний endpoint
    } else {
        console.error("Невідомий тип контенту");
        return;
    }

    fetch(endpoint)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Помилка: " + data.error);
                return;
            }
            const modalLabel = document.getElementById('newsModalLabel');
            const modalBody = document.getElementById('newsModalBody');
            if (!modalLabel || !modalBody) {
                console.error("Модалка не знайдена у DOM!");
                return;
            }
            modalLabel.innerText = data.title;
            modalBody.innerHTML = `
                ${data.image ? `<img src="${data.image}" alt="${data.title}" class="img-fluid mb-3">` : ""}
                <p>${data.content}</p>
            `;
            const modal = new bootstrap.Modal(document.getElementById('newsModal'));
            modal.show();
        })
        .catch(err => {
            console.error("Помилка завантаження детального контенту:", err);
            alert("Не вдалося завантажити повний вміст.");
        });
}

    
});
