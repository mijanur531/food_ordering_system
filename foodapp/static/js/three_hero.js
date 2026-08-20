/**
 * FoodVibe Three.js 3D Interactive Hero Scene
 * Renders an interactive 3D stylized gourmet dish / burger with dynamic lighting,
 * particle sparkle effects, and mouse/touch responsiveness.
 */

(function () {
  'use strict';

  function initThreeHero() {
    const container = document.getElementById('threejs-hero-container');
    if (!container || typeof THREE === 'undefined') return;

    const width = container.clientWidth;
    const height = container.clientHeight || 450;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 1.2, 5.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Master Dish Group
    const dishGroup = new THREE.Group();
    scene.add(dishGroup);

    // Materials
    const bunMaterial = new THREE.MeshStandardMaterial({
      color: 0xdf9344,
      roughness: 0.4,
      metalness: 0.1,
    });
    const pattyMaterial = new THREE.MeshStandardMaterial({
      color: 0x5a2d18,
      roughness: 0.8,
      metalness: 0.05,
    });
    const cheeseMaterial = new THREE.MeshStandardMaterial({
      color: 0xffb703,
      roughness: 0.3,
      metalness: 0.1,
    });
    const lettuceMaterial = new THREE.MeshStandardMaterial({
      color: 0x22c55e,
      roughness: 0.6,
      metalness: 0.1,
    });
    const tomatoMaterial = new THREE.MeshStandardMaterial({
      color: 0xef4444,
      roughness: 0.2,
      metalness: 0.1,
    });
    const plateMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.1,
      metalness: 0.15,
    });

    // 1. Ceramic Serving Plate
    const plateGeo = new THREE.CylinderGeometry(2.1, 1.8, 0.12, 48);
    const plate = new THREE.Mesh(plateGeo, plateMaterial);
    plate.position.y = -1.1;
    plate.receiveShadow = true;
    dishGroup.add(plate);

    // Inner rim
    const rimGeo = new THREE.TorusGeometry(2.0, 0.06, 16, 48);
    const rim = new THREE.Mesh(rimGeo, new THREE.MeshStandardMaterial({ color: 0xff5e3a, roughness: 0.3 }));
    rim.rotation.x = Math.PI / 2;
    rim.position.y = -1.04;
    dishGroup.add(rim);

    // 2. Bottom Bun
    const bottomBunGeo = new THREE.CylinderGeometry(1.25, 1.15, 0.35, 32);
    const bottomBun = new THREE.Mesh(bottomBunGeo, bunMaterial);
    bottomBun.position.y = -0.8;
    bottomBun.castShadow = true;
    bottomBun.receiveShadow = true;
    dishGroup.add(bottomBun);

    // 3. Crisp Veg/Paneer/Patty Layer
    const pattyGeo = new THREE.CylinderGeometry(1.3, 1.3, 0.38, 32);
    const patty = new THREE.Mesh(pattyGeo, pattyMaterial);
    patty.position.y = -0.42;
    patty.castShadow = true;
    dishGroup.add(patty);

    // 4. Melted Cheese Slice (angled square)
    const cheeseGeo = new THREE.BoxGeometry(1.7, 0.08, 1.7);
    const cheese = new THREE.Mesh(cheeseGeo, cheeseMaterial);
    cheese.position.y = -0.18;
    cheese.rotation.y = Math.PI / 4;
    cheese.castShadow = true;
    dishGroup.add(cheese);

    // 5. Fresh Tomato Slices
    const tomato1 = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.1, 24), tomatoMaterial);
    tomato1.position.set(-0.45, 0.02, -0.2);
    tomato1.rotation.z = 0.05;
    tomato1.castShadow = true;
    dishGroup.add(tomato1);

    const tomato2 = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.1, 24), tomatoMaterial);
    tomato2.position.set(0.45, 0.04, 0.2);
    tomato2.rotation.z = -0.05;
    tomato2.castShadow = true;
    dishGroup.add(tomato2);

    // 6. Wavy Fresh Lettuce Ring
    const lettuceGroup = new THREE.Group();
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2;
      const leafGeo = new THREE.SphereGeometry(0.45, 12, 12);
      leafGeo.scale(1.2, 0.25, 0.7);
      const leaf = new THREE.Mesh(leafGeo, lettuceMaterial);
      leaf.position.set(Math.cos(angle) * 1.05, 0.2, Math.sin(angle) * 1.05);
      leaf.rotation.y = angle + Math.PI / 2;
      leaf.rotation.z = 0.2 * Math.sin(i);
      leaf.castShadow = true;
      lettuceGroup.add(leaf);
    }
    dishGroup.add(lettuceGroup);

    // 7. Top Golden Sesame Bun
    const topBunGeo = new THREE.SphereGeometry(1.3, 32, 24, 0, Math.PI * 2, 0, Math.PI / 2);
    topBunGeo.scale(1, 0.65, 1);
    const topBun = new THREE.Mesh(topBunGeo, bunMaterial);
    topBun.position.y = 0.35;
    topBun.castShadow = true;
    dishGroup.add(topBun);

    // 8. Sesame Seeds on top bun
    const sesameMat = new THREE.MeshStandardMaterial({ color: 0xfff3d6, roughness: 0.3 });
    const sesameGeo = new THREE.ConeGeometry(0.03, 0.07, 6);
    for (let i = 0; i < 30; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.random() * (Math.PI / 3);
      const r = 1.28;
      const seed = new THREE.Mesh(sesameGeo, sesameMat);
      seed.position.set(
        r * Math.sin(phi) * Math.cos(theta),
        0.35 + r * Math.cos(phi) * 0.62,
        r * Math.sin(phi) * Math.sin(theta)
      );
      seed.rotation.x = Math.random() * Math.PI;
      dishGroup.add(seed);
    }

    // 9. Floating Particle Ingredients & Sparkles
    const particleCount = 45;
    const particleGeo = new THREE.DodecahedronGeometry(0.06, 0);
    const particleMat = new THREE.MeshStandardMaterial({
      color: 0xff7e5f,
      roughness: 0.2,
      emissive: 0xff5e3a,
      emissiveIntensity: 0.3,
    });

    const particles = [];
    for (let i = 0; i < particleCount; i++) {
      const p = new THREE.Mesh(particleGeo, particleMat);
      const radius = 2.2 + Math.random() * 1.5;
      const theta = Math.random() * Math.PI * 2;
      const py = -0.8 + Math.random() * 2.4;
      p.position.set(radius * Math.cos(theta), py, radius * Math.sin(theta));
      p.userData = {
        speed: 0.005 + Math.random() * 0.01,
        angle: theta,
        radius: radius,
        baseY: py,
        floatFreq: 1 + Math.random() * 2,
      };
      scene.add(p);
      particles.push(p);
    }

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffeedd, 1.4);
    dirLight.position.set(5, 8, 5);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    scene.add(dirLight);

    const pointLight = new THREE.PointLight(0xff5e3a, 1.2, 12);
    pointLight.position.set(-3, 2, 3);
    scene.add(pointLight);

    const rimLight = new THREE.DirectionalLight(0x60a5fa, 0.6);
    rimLight.position.set(0, -4, -4);
    scene.add(rimLight);

    // Mouse & Touch Interactivity
    let targetRotationX = 0.25;
    let targetRotationY = 0;
    let mouseX = 0;
    let mouseY = 0;
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    container.addEventListener('mousemove', function (e) {
      const rect = container.getBoundingClientRect();
      mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouseY = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
      targetRotationY = mouseX * 0.8;
      targetRotationX = 0.25 - mouseY * 0.4;
    });

    container.addEventListener('mousedown', function (e) {
      isDragging = true;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', function () {
      isDragging = false;
    });

    window.addEventListener('mousemove', function (e) {
      if (!isDragging) return;
      const deltaX = e.clientX - previousMousePosition.x;
      const deltaY = e.clientY - previousMousePosition.y;
      dishGroup.rotation.y += deltaX * 0.01;
      dishGroup.rotation.x += deltaY * 0.01;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    // Touch support for mobile devices
    container.addEventListener('touchmove', function (e) {
      if (e.touches.length > 0) {
        const touch = e.touches[0];
        const rect = container.getBoundingClientRect();
        mouseX = ((touch.clientX - rect.left) / rect.width) * 2 - 1;
        mouseY = -(((touch.clientY - rect.top) / rect.height) * 2 - 1);
        targetRotationY = mouseX * 0.8;
        targetRotationX = 0.25 - mouseY * 0.4;
      }
    }, { passive: true });

    // Handle Window Resizing
    function onWindowResize() {
      if (!container) return;
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight || 450;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    }
    window.addEventListener('resize', onWindowResize);

    // Animation Loop
    let clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Gentle floating hover motion
      dishGroup.position.y = Math.sin(elapsedTime * 1.5) * 0.08;

      if (!isDragging) {
        // Continuous slow rotation + smooth easing to mouse target
        targetRotationY += 0.003;
        dishGroup.rotation.y += (targetRotationY - dishGroup.rotation.y) * 0.05;
        dishGroup.rotation.x += (targetRotationX - dishGroup.rotation.x) * 0.05;
      }

      // Animate floating particles
      particles.forEach(function (p) {
        p.userData.angle += p.userData.speed;
        p.position.x = p.userData.radius * Math.cos(p.userData.angle);
        p.position.z = p.userData.radius * Math.sin(p.userData.angle);
        p.position.y = p.userData.baseY + Math.sin(elapsedTime * p.userData.floatFreq) * 0.15;
        p.rotation.x += 0.02;
        p.rotation.y += 0.03;
      });

      renderer.render(scene, camera);
    }

    animate();
  }

  // Initialize once DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThreeHero);
  } else {
    initThreeHero();
  }
})();
