let currentPage = 1;
let totalPages = 1;
let players = {};

function createVideoCard(video) {
    const card = document.createElement("div");
    card.className = "video-card";
    const iframeId = `ytplayer-${video.yt_id}`;
    card.innerHTML = `
        <div class="video-player">
            <iframe id="${iframeId}"
                    src="https://www.youtube.com/embed/${video.yt_id}?enablejsapi=1&modestbranding=1&rel=0&controls=0" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
            <div class="video-overlay">
                <button class="exit-fullscreen hidden">✖</button>
            </div>
        </div>
        <div class="video-controls">
            <button class="play">▶</button>
            <button class="pause">⏸</button>
            <button class="forward">+10s</button>
            <button class="fullscreen">⛶</button>
            <button class="exit-fullscreen hidden">✖</button>
        </div>
        <div class="video-info">
            <h2>${video.title}</h2>
            <p>${video.description || ""}</p>
        </div>
    `;
    return card;
}


function onYouTubeIframeAPIReady() {
    document.querySelectorAll('.video-card').forEach(card => {
        const iframe = card.querySelector('iframe');
        if (!iframe) return;

        const player = new YT.Player(iframe.id);
        players[iframe.id] = player;

        const playBtn = card.querySelector('.play');
        const pauseBtn = card.querySelector('.pause');
        const forwardBtn = card.querySelector('.forward');
        const fsBtn = card.querySelector('.fullscreen');

        playBtn.addEventListener('click', () => player.playVideo());
        pauseBtn.addEventListener('click', () => player.pauseVideo());
        forwardBtn.addEventListener('click', () => {
            const currentTime = player.getCurrentTime();
            player.seekTo(currentTime + 10, true);
        });

        fsBtn.addEventListener('click', () => {
            const container = card.querySelector('.video-player');
            if (container.requestFullscreen) {
                container.requestFullscreen();
            } else if (container.webkitRequestFullscreen) {
                container.webkitRequestFullscreen();
            } else if (container.mozRequestFullScreen) {
                container.mozRequestFullScreen();
            } else if (container.msRequestFullscreen) {
                container.msRequestFullscreen();
            }
        });

        const exitFsBtn = card.querySelector('.exit-fullscreen');
        exitFsBtn.addEventListener('click', () => {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        });
    });
}

document.addEventListener("fullscreenchange", () => {
    if (document.fullscreenElement) {
        document.querySelectorAll('.exit-fullscreen').forEach(btn => btn.classList.remove('hidden'));
    } else {
        document.querySelectorAll('.exit-fullscreen').forEach(btn => btn.classList.add('hidden'));
    }
});



function onPlayerStateChange(event) {
    const card = event.target.getIframe().closest('.video-card');

    if (event.data === YT.PlayerState.PLAYING) {
        card.querySelector('.video-player').classList.add('playing');
    } else if (event.data === YT.PlayerState.PAUSED || event.data === YT.PlayerState.ENDED) {
        card.querySelector('.video-player').classList.remove('playing');
    }
}

async function loadVideos(page = 1, faculty = "") {
    try {
        const response = await fetch(`api/videos?page=${page}&faculty=${encodeURIComponent(faculty)}`);
        const data = await response.json();
        const container = document.getElementById("video-container");
        container.innerHTML = "";

        if (!data.videos.length) {
            container.innerHTML = "<p>Немає відео для цього факультету</p>";
            return;
        }

        data.videos.forEach(video => container.appendChild(createVideoCard(video)));

        onYouTubeIframeAPIReady();

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
