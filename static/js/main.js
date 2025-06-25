document.addEventListener('DOMContentLoaded', () => {
    // Переключение темы
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    themeToggle.addEventListener('click', () => {
        const isDark = html.getAttribute('data-theme') === 'dark';
        html.setAttribute('data-theme', isDark ? 'light' : 'dark');
        themeToggle.innerHTML = isDark 
            ? '<i class="fas fa-moon"></i>' 
            : '<i class="fas fa-sun"></i>';
        
        localStorage.setItem('theme', isDark ? 'light' : 'dark');
    });
    
    // Восстановление темы
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    themeToggle.innerHTML = savedTheme === 'dark' 
        ? '<i class="fas fa-sun"></i>' 
        : '<i class="fas fa-moon"></i>';
    
    // Анимация отправки формы
    const form = document.getElementById('chat-form');
    const submitBtn = document.getElementById('submit-btn');
    
    form.addEventListener('submit', () => {
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Обработка...';
        submitBtn.disabled = true;
    });
    
    // Плавная прокрутка к новым сообщениям
    const chatHistory = document.getElementById('chat-history');
    const observer = new MutationObserver(() => {
        chatHistory.scrollTo({
            top: chatHistory.scrollHeight,
            behavior: 'smooth'
        });
    });
    
    observer.observe(chatHistory, { childList: true });
    
    // Подсветка кода в ответах (если есть)
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
});