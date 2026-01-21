class ThemeManager {
    constructor() {
        this.themes = ['github-dark', 'github-light', 'dracula', 'nord'];
        this.currentTheme = localStorage.getItem('theme') || 'github-dark';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createThemeSelector();
    }

    applyTheme(theme) {
        document.documentElement.className = theme;
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;

        // Отправляем на сервер если пользователь авторизован
        if (window.userIsAuthenticated) {
            fetch('/api/update-theme/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ theme: theme })
            });
        }
    }

    createThemeSelector() {
        const selector = document.createElement('div');
        selector.className = 'theme-selector fixed bottom-4 right-4 z-50';
        selector.innerHTML = `
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-4">
                <h4 class="font-bold mb-3">Тема</h4>
                <div class="grid grid-cols-2 gap-2">
                    ${this.themes.map(theme => `
                        <button class="theme-btn p-3 rounded border ${theme === this.currentTheme ? 'ring-2 ring-blue-500' : ''}"
                                data-theme="${theme}">
                            <div class="w-6 h-6 rounded ${theme === 'github-dark' ? 'bg-gray-900' :
                                                      theme === 'github-light' ? 'bg-white border' :
                                                      theme === 'dracula' ? 'bg-purple-900' : 'bg-blue-900'}"></div>
                            <span class="text-xs mt-1">${theme.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}</span>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(selector);

        selector.querySelectorAll('.theme-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const theme = e.currentTarget.dataset.theme;
                this.applyTheme(theme);
                this.updateActiveButton(theme);
            });
        });
    }

    updateActiveButton(theme) {
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.toggle('ring-2 ring-blue-500', btn.dataset.theme === theme);
        });
    }
}
