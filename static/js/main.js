let idleTimeout;
const IDLE_TIME = 60000; 
const IDLE_VIDEO_YOUTUBE_ID = "21g4f9jJt9o"; 

function showIdleVideo() {
    const overlay = document.createElement("div");
    overlay.id = "idle-overlay";
    overlay.innerHTML = `
        <div class="video-wrapper">
            <iframe src="https://www.youtube.com/embed/${IDLE_VIDEO_YOUTUBE_ID}?autoplay=1&mute=1" 
                    frameborder="0" 
                    allow="autoplay; encrypted-media; picture-in-picture" 
                    allowfullscreen>
            </iframe>
        </div>
    `;

    document.body.appendChild(overlay);
    
    document.addEventListener("mousemove", hideIdleVideo);
    document.addEventListener("touchstart", hideIdleVideo);
    document.addEventListener("keydown", hideIdleVideo);
}

function hideIdleVideo() {
    const overlay = document.getElementById("idle-overlay");
    if (overlay) {
        overlay.remove();
        document.removeEventListener("mousemove", hideIdleVideo);
        document.removeEventListener("touchstart", hideIdleVideo);
        document.removeEventListener("keydown", hideIdleVideo);
    }
    resetIdleTimer();
}

function resetIdleTimer() {
    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(showIdleVideo, IDLE_TIME);
}

document.addEventListener("DOMContentLoaded", resetIdleTimer);

document.addEventListener("mousemove", resetIdleTimer);
document.addEventListener("touchstart", resetIdleTimer);
document.addEventListener("keydown", resetIdleTimer);

document.addEventListener("DOMContentLoaded", () => {
    console.log("main.js завантажено");

    const facultyLinks = document.querySelectorAll(".faculty-link");
    facultyLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const facultyId = link.dataset.facultyId;
            window.location.href = `/video?faculty=${facultyId}`;
        });
    });

    });



    

