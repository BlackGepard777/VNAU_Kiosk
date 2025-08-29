let currentPage = 1;
let totalPages = 1;

function createVideoCard(video) {
    const card = document.createElement("div");
    card.className = "video-card";
    card.innerHTML = `
        <div class="video-player">
            <iframe src="https://www.youtube.com/embed/${video.yt_id}" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
        </div>
        <div class="video-info">
            <h2>${video.title}</h2>
            <p>${video.description || ""}</p>
        </div>
    `;
    return card;
}

async function loadVideos(page = 1, faculty = "") {
    try {
        const response = await fetch(`/api/videos?page=${page}&faculty=${encodeURIComponent(faculty)}`);
        const data = await response.json();
        const container = document.getElementById("video-container");
        container.innerHTML = "";

        if (!data.videos.length) {
            container.innerHTML = "<p>Немає відео для цього факультету</p>";
            return;
        }

        data.videos.forEach(video => container.appendChild(createVideoCard(video)));

        currentPage = data.page;
        totalPages = data.pages;
        document.getElementById("page-info").textContent = `Сторінка ${currentPage} з ${totalPages}`;
        document.getElementById("prev").disabled = currentPage <= 1;
        document.getElementById("next").disabled = currentPage >= totalPages;
    } catch (err) {
        console.error("Помилка завантаження відео:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const faculty = urlParams.get("faculty") || "";

    loadVideos(1, faculty);

    document.getElementById("prev").addEventListener("click", () => {
        if (currentPage > 1) loadVideos(currentPage - 1, faculty);
    });
    document.getElementById("next").addEventListener("click", () => {
        if (currentPage < totalPages) loadVideos(currentPage + 1, faculty);
    });
});
