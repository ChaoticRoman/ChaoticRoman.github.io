let scene, camera, renderer, points, geometry, material;

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000); // Black background

    document.body.appendChild(renderer.domElement);
    renderer.domElement.style.position = "fixed";
    renderer.domElement.style.top = "0";
    renderer.domElement.style.left= "0";
    renderer.domElement.style.zIndex= "-1";

    geometry = new THREE.BufferGeometry();
    const vertices = [];
    const numPoints = 1000;

    // Generate random points
    for (let i = 0; i < numPoints; i++) {
        vertices.push((Math.random() - 0.5) * 10); // x
        vertices.push((Math.random() - 0.5) * 10); // y
        vertices.push((Math.random() - 0.5) * 10); // z
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

    material = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.01 });

    points = new THREE.Points(geometry, material);
    scene.add(points);

    camera.position.z = 5;

    animate();
}

function animate() {
    requestAnimationFrame(animate);

    points.rotation.x += 0.001;
    points.rotation.y += 0.001;

    renderer.render(scene, camera);
}

window.addEventListener('resize', function() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});

init();
