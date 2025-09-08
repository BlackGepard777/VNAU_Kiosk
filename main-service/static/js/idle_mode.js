document.addEventListener('DOMContentLoaded', () => {
    let idleTimeout;
    const IDLE_TIME = 600000; 

    function redirectToIdlePage() {
        fetch("/api/idle_video")
            .then(response => {
                if (response.status === 200) {
                    window.location.href = '/idle';
                }
            })
            .catch(error => {
                console.error("Помилка при перевірці відео бездіяльності:", error);
            });
    }

    function resetIdleTimer() {
        clearTimeout(idleTimeout);
        idleTimeout = setTimeout(redirectToIdlePage, IDLE_TIME);
    }

    document.addEventListener("mousemove", resetIdleTimer);
    document.addEventListener("touchstart", resetIdleTimer);
    document.addEventListener("keydown", resetIdleTimer);
    
    resetIdleTimer(); 
});