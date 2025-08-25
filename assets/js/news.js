document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');
    fetch('/api/news').then(res => res.json()).then(news => {
        news.forEach(item => { /* код для відображення новин */ });
    }).catch(err => console.error(err));
});