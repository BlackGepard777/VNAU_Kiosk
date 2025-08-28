// === main.js ===
// Виконується тільки на головній сторінці (розклад, факультети і т.д.)

document.addEventListener("DOMContentLoaded", () => {
    console.log("main.js завантажено");

    // Перехід на сторінку відео певного факультету
    const facultyLinks = document.querySelectorAll(".faculty-link");
    facultyLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const facultyId = link.dataset.facultyId;
            window.location.href = `/video?faculty=${facultyId}`;
        });
    });

    });



    

