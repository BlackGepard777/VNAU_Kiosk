// Функція для завантаження контенту
function loadPage(pageName) {
    const appContainer = document.getElementById('app-container');

    const filePath = pageName === 'index' ? `/${pageName}.html` : `/pages/${pageName}.html`;

    fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Помилка: ${response.status} ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            // Очищаємо контейнер перед додаванням нового контенту
            appContainer.innerHTML = html;

            // Динамічне завантаження скриптів
            if (pageName === 'videos') {
                const script = document.createElement('script');
                script.src = `assets/js/${pageName}.js`;
                script.onload = () => {
                    // Після завантаження скрипту, викликаємо функцію
                    if (typeof initVideosPage === 'function') {
                        initVideosPage();
                    }
                };
                appContainer.appendChild(script);
            }
        })
        .catch(error => {
            console.error('Помилка завантаження сторінки:', error);
            appContainer.innerHTML = `<div style="text-align:center; padding: 50px;">
                                        <p>Не вдалося завантажити сторінку. Спробуйте пізніше.</p>
                                      </div>`;
        });
}

// Завантаження головної сторінки при першому запуску
window.addEventListener('load', () => {
    loadPage('index');
});