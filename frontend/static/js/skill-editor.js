// skill-editor.js - Drag & Drop редактор навыков
class SkillEditor {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.skills = [];
        this.editingSkill = null;
        this.init();
    }

    init() {
        this.render();
        this.loadSkills();
    }

    async loadSkills() {
        // Загружаем навыки через API
        try {
            const response = await fetch('/api/skills/');
            this.skills = await response.json();
            this.renderSkills();
        } catch (error) {
            console.error('Error loading skills:', error);
        }
    }

    render() {
        this.container.innerHTML = `
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <h3 class="text-xl font-bold mb-4">Редактор навыков</h3>

                <!-- Форма добавления навыка -->
                <div class="mb-6 p-4 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
                    <h4 class="font-semibold mb-3">Добавить навык</h4>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <input type="text" id="skill-name"
                               class="p-2 border rounded dark:bg-gray-700"
                               placeholder="Название навыка">

                        <select id="skill-category" class="p-2 border rounded dark:bg-gray-700">
                            <option value="frontend">Frontend</option>
                            <option value="backend">Backend</option>
                            <option value="tools">Tools & DevOps</option>
                            <option value="soft">Soft Skills</option>
                        </select>

                        <div class="flex items-center gap-2">
                            <span>Уровень:</span>
                            <div class="flex items-center">
                                ${[1,2,3,4,5].map(i => `
                                    <button type="button"
                                            class="level-btn w-8 h-8 rounded-full border mx-1
                                                   ${i === 3 ? 'bg-blue-500 text-white' : 'bg-gray-100 dark:bg-gray-700'}"
                                            data-level="${i}">
                                        ${i}
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <div class="mt-4 flex gap-2">
                        <button id="add-skill-btn"
                                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
                            Добавить
                        </button>
                        <button id="save-skill-btn"
                                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 hidden">
                            Сохранить
                        </button>
                    </div>
                </div>

                <!-- Список навыков -->
                <div id="skills-list" class="space-y-3"></div>
            </div>
        `;

        this.bindEvents();
    }

    bindEvents() {
        // Кнопки уровня
        document.querySelectorAll('.level-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.level-btn').forEach(b =>
                    b.classList.remove('bg-blue-500', 'text-white'));
                e.target.classList.add('bg-blue-500', 'text-white');
            });
        });

        // Добавление навыка
        document.getElementById('add-skill-btn').addEventListener('click', () => this.addSkill());
        document.getElementById('save-skill-btn').addEventListener('click', () => this.saveSkill());
    }

    async addSkill() {
        const name = document.getElementById('skill-name').value.trim();
        const category = document.getElementById('skill-category').value;
        const level = document.querySelector('.level-btn.bg-blue-500')?.dataset.level || 3;

        if (!name) {
            alert('Введите название навыка');
            return;
        }

        const skill = { name, category, level: parseInt(level) };

        try {
            const response = await fetch('/api/skills/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(skill)
            });

            if (response.ok) {
                this.skills.push(await response.json());
                this.renderSkills();
                this.clearForm();
            }
        } catch (error) {
            console.error('Error adding skill:', error);
        }
    }

    renderSkills() {
        const container = document.getElementById('skills-list');
        if (!container) return;

        container.innerHTML = this.skills.map((skill, index) => `
            <div class="skill-item flex items-center justify-between p-3
                        bg-gray-50 dark:bg-gray-900 rounded-lg"
                 draggable="true" data-index="${index}">
                <div class="flex items-center gap-4">
                    <div class="drag-handle cursor-move text-gray-400">⋮⋮</div>
                    <div>
                        <div class="font-medium">${skill.name}</div>
                        <div class="text-sm text-gray-500">${skill.category} • Уровень ${skill.level}/5</div>
                    </div>
                </div>
                <div class="flex gap-2">
                    <button class="edit-btn px-3 py-1 bg-yellow-500 text-white rounded text-sm">
                        ✏️
                    </button>
                    <button class="delete-btn px-3 py-1 bg-red-500 text-white rounded text-sm">
                        🗑️
                    </button>
                </div>
            </div>
        `).join('');

        // Добавляем обработчики событий
        this.addSkillItemEvents();
        this.setupDragAndDrop();
    }

    addSkillItemEvents() {
        document.querySelectorAll('.edit-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => this.editSkill(index));
        });

        document.querySelectorAll('.delete-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => this.deleteSkill(index));
        });
    }

    setupDragAndDrop() {
        const container = document.getElementById('skills-list');
        let draggedItem = null;

        container.querySelectorAll('.skill-item').forEach(item => {
            item.addEventListener('dragstart', (e) => {
                draggedItem = item;
                setTimeout(() => item.classList.add('opacity-50'), 0);
            });

            item.addEventListener('dragend', () => {
                draggedItem = null;
                item.classList.remove('opacity-50');
            });
        });

        container.addEventListener('dragover', (e) => {
            e.preventDefault();
            const afterElement = this.getDragAfterElement(container, e.clientY);

            if (afterElement == null) {
                container.appendChild(draggedItem);
            } else {
                container.insertBefore(draggedItem, afterElement);
            }
        });
    }

    getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.skill-item:not(.opacity-50)')];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;

            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    editSkill(index) {
        const skill = this.skills[index];
        this.editingSkill = { index, ...skill };

        document.getElementById('skill-name').value = skill.name;
        document.getElementById('skill-category').value = skill.category;

        document.querySelectorAll('.level-btn').forEach(btn => {
            btn.classList.toggle('bg-blue-500 text-white',
                parseInt(btn.dataset.level) === skill.level);
        });

        document.getElementById('add-skill-btn').classList.add('hidden');
        document.getElementById('save-skill-btn').classList.remove('hidden');
    }

    async saveSkill() {
        if (!this.editingSkill) return;

        const name = document.getElementById('skill-name').value.trim();
        const category = document.getElementById('skill-category').value;
        const level = document.querySelector('.level-btn.bg-blue-500')?.dataset.level || 3;

        const updatedSkill = { ...this.editingSkill, name, category, level: parseInt(level) };

        try {
            const response = await fetch(`/api/skills/${updatedSkill.id}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedSkill)
            });

            if (response.ok) {
                this.skills[this.editingSkill.index] = await response.json();
                this.renderSkills();
                this.clearForm();
                this.editingSkill = null;
            }
        } catch (error) {
            console.error('Error saving skill:', error);
        }
    }

    async deleteSkill(index) {
        const skill = this.skills[index];

        if (confirm(`Удалить навык "${skill.name}"?`)) {
            try {
                const response = await fetch(`/api/skills/${skill.id}/`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    this.skills.splice(index, 1);
                    this.renderSkills();
                }
            } catch (error) {
                console.error('Error deleting skill:', error);
            }
        }
    }

    clearForm() {
        document.getElementById('skill-name').value = '';
        document.querySelectorAll('.level-btn').forEach((btn, i) => {
            btn.classList.toggle('bg-blue-500 text-white', i === 2); // level 3 по умолчанию
        });

        document.getElementById('add-skill-btn').classList.remove('hidden');
        document.getElementById('save-skill-btn').classList.add('hidden');
    }
}
