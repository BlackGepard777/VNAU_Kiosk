const facultySelect = document.getElementById("facultySelect");
    const courseSelect = document.getElementById("courseSelect");
    const groupSelect = document.getElementById("groupSelect");
    const scheduleContainer = document.getElementById("schedule");

    async function loadFaculties() {
      const res = await fetch("https://mkr.sergkh.com/structures/0/faculties");
      const faculties = await res.json();

      facultySelect.innerHTML = '<option value="">Select a faculty</option>';
      faculties.forEach(f => {
        const option = document.createElement("option");
        option.value = f.id;
        option.textContent = f.name;
        facultySelect.appendChild(option);
      });
    }

    async function loadCourses(facultyId) {
      courseSelect.innerHTML = '<option value="">Loading courses...</option>';
      groupSelect.innerHTML = '<option>Select a course</option>';
      const res = await fetch(`https://mkr.sergkh.com/structures/0/faculties/${facultyId}/courses`);
      const courses = await res.json();

      courseSelect.innerHTML = '<option value="">Select a course</option>';
      courses.forEach(c => {
        const option = document.createElement("option");
        option.value = c.id;
        option.textContent = c.name;
        courseSelect.appendChild(option);
      });
    }

    async function loadGroups(facultyId, courseId) {
      groupSelect.innerHTML = '<option value="">Loading a groups...</option>';
      const res = await fetch(`https://mkr.sergkh.com/structures/0/faculties/${facultyId}/courses/${courseId}/groups`);
      const groups = await res.json();

      groupSelect.innerHTML = '<option value="">Select a group</option>';
      groups.forEach(g => {
        const option = document.createElement("option");
        option.value = g.id;
        option.textContent = g.name;
        groupSelect.appendChild(option);
      });
    }

    async function loadSchedule(groupId) {
    scheduleContainer.innerHTML = "Loading...";
    try {
        const res = await fetch(`https://mkr.sergkh.com/structures/0/faculties/0/courses/0/groups/${groupId}/schedule`);
        const data = await res.json();

        const grouped = {};
        data.forEach(item => {
            const date = new Date(item.start).toLocaleDateString("uk-UA", { weekday: "long", year: "numeric", month: "long", day: "numeric" });
            if (!grouped[date]) grouped[date] = [];
            grouped[date].push(item);
        });

        scheduleContainer.innerHTML = "";
        for (const [date, lessons] of Object.entries(grouped)) {
            const dayDiv = document.createElement("div");
            dayDiv.className = "day";

            const h2 = document.createElement("h2");
            h2.textContent = `Schedule for ${date}`;
            dayDiv.appendChild(h2);

            lessons.forEach(item => {
              const div = document.createElement("div");
              div.className = "lesson";
              let lessonTypeClass = '';
              const lessonType = item.type.toLowerCase();

              if (lessonType.includes("лекція") || lessonType.includes("lection")) {
                  lessonTypeClass = 'lesson-type-lection';
              } else if (lessonType.includes("практика") || lessonType.includes("practice")) {
                  lessonTypeClass = 'lesson-type-practice';
              } else if (lessonType.includes("екзамен") || lessonType.includes("exam")) {
                  lessonTypeClass = 'lesson-type-lab';
              } else if (lessonType.includes("залік") || lessonType.includes("zalik")) {
                  lessonTypeClass = 'lesson-type-lab';
              } else {
                  lessonTypeClass = 'lesson-type-other';
              }

              div.classList.add(lessonTypeClass);

              div.innerHTML = `
              <div class="lesson-time">
                ${new Date(item.start).toLocaleTimeString("uk-UA", { hour: "2-digit", minute: "2-digit" })}
              </div>
              <div class="lesson-content">
                <h3 class="lesson-name">
                  <span class="icon">
                    ${item.type === "lection" ? "📖" : item.type === "practice" ? "🧑‍🏫" : item.type === "Лб" ? "💻" : "📌"}
                  </span>
                  ${item.name}
                </h3>
                <div class="meta">
                  Викладач: ${item.teacher} <br>
                  Аудиторія: ${item.place}
                </div>
              </div>
            `;

              dayDiv.appendChild(div);
          });

          scheduleContainer.appendChild(dayDiv);
        }
    } catch (error) {
        console.error("Помилка завантаження розкладу:", error);
        scheduleContainer.innerHTML = `<p class="error-message">Не вдалося завантажити розклад. Спробуйте пізніше.</p>`;
    }
}

    facultySelect.addEventListener("change", () => {
      if(facultySelect.value) loadCourses(facultySelect.value);
    });

    courseSelect.addEventListener("change", () => {
      if(courseSelect.value && facultySelect.value) loadGroups(facultySelect.value, courseSelect.value);
    });

    groupSelect.addEventListener("change", () => {
      if(groupSelect.value) loadSchedule(groupSelect.value);
    });

    loadFaculties();