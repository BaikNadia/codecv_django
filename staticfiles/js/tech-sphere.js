// tech-sphere.js - 3D визуализация технологий
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

class TechSphere {
    constructor(containerId, technologies = []) {
        this.container = document.getElementById(containerId);
        this.technologies = technologies;

        // Настройка сцены
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

        this.init();
        this.animate();
    }

    init() {
        // Настройка рендерера
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);

        // Позиция камеры
        this.camera.position.z = 5;

        // Orbit controls
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;

        // Освещение
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        this.scene.add(directionalLight);

        // Создание сферы с точками
        this.createSphere();

        // Обработчик изменения размера
        window.addEventListener('resize', () => this.onWindowResize());
    }

    createSphere() {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const colors = [];

        // Создаем точки на сфере
        const radius = 2;
        const numPoints = this.technologies.length || 20;

        for (let i = 0; i < numPoints; i++) {
            const phi = Math.acos(-1 + (2 * i) / numPoints);
            const theta = Math.sqrt(numPoints * Math.PI) * phi;

            const x = radius * Math.sin(phi) * Math.cos(theta);
            const y = radius * Math.sin(phi) * Math.sin(theta);
            const z = radius * Math.cos(phi);

            vertices.push(x, y, z);

            // Цвета для точек
            colors.push(
                Math.random() * 0.5 + 0.5,  // R
                Math.random() * 0.5 + 0.5,  // G
                Math.random() * 0.5 + 0.5   // B
            );
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.1,
            vertexColors: true,
            transparent: true,
            opacity: 0.8
        });

        this.sphere = new THREE.Points(geometry, material);
        this.scene.add(this.sphere);
    }

    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.sphere) {
            this.sphere.rotation.y += 0.001;
        }

        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }

    updateTechnologies(technologies) {
        this.technologies = technologies;
        // Пересоздаем сферу с новыми технологиями
        this.scene.remove(this.sphere);
        this.createSphere();
    }
}

// Экспортируем для использования
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TechSphere;
} else {
    window.TechSphere = TechSphere;
}
