---
title: romanpavelka.cz
description: personal webpage
---

[Short bio](https://github.com/ChaoticRoman/ChaoticRoman/blob/main/README.md)  
Phone number: [+420 736 452 265](tel:+420736452265)  
E-mail: [roman.pavelka.asi@gmail.com](mailto:roman.pavelka.asi@gmail.com)  
Github: [ChaoticRoman](https://github.com/ChaoticRoman)  
Codewars: [ChaoticRoman](https://www.codewars.com/users/ChaoticRoman/)  
LinkedIn: [Roman Pavelka](https://www.linkedin.com/in/roman-pavelka-b721339b/)  
<a rel="me" href="https://toot.cat/@ChaoticRoman">Mastodon</a>: @ChaoticRoman@toot.cat  
Stack Overflow: [Roman Pavelka](https://stackoverflow.com/users/12118546/roman-pavelka)  
IČO: [10763589](zivnost.pdf)  
DIČ: CZ8805267801  
Důchodové pojištění (variabilní symbol): 75664501  
Číslo účtu: [1026116241/5500 (Raiffeisenbank)](qr.png)  
IBAN: CZ6655000000001026116241  
XCH wallet: xch1nqw477dvxqm89dem92rxsgapyxc7203mwft8gpzxujkasvkej3fsvk0wnj  
[CV in English \[Google doc\]](https://docs.google.com/document/d/1chWjWus-AKZ4OC9tiD6cijwMMeaZSnZuHH4SbBLnbwY)  
[CV in Czech \[Google doc\]](https://docs.google.com/document/d/1kjOD4RH9kXEZwlxmo9bSw1o4J6N0vOD-g8OP7KHNMnA)  
[Picture of me \[JPEG\]](rpavelka.jpg)  
[Bachelor thesis \[PDF\]](fluxgate.pdf),
[review by supervisor \[PDF\]](Review_Roman_Pavelka.pdf),
[oponnent review \[PDF\]](Roman_bw.pdf)  
[Bachelor degree diploma \[PDF\]](diplom.pdf), [diploma supplement \[PDF\]](dodatek.pdf)  
[Sizes](sizes), [Meds](meds)  

## Topics

<a href='kurzy'>Kurzy</a><br>
<a href='kicad'>KiCad</a><br>
<a href='pi'>Raspberry Pi</a><br>
<a href='net'>Networking</a><br>
<a href='bash'>Bash</a><br>
<a href='python'>Python</a><br>
<a href='https://docs.google.com/document/d/1_MJSi8OFwptRwPrKsqrWDVxT5rG6KoHWJWzKFEDcVgE'>C++ tricks [Google doc]</a><br>
<a href='https://docs.google.com/document/d/1R2KTPmzWfuTrcC5v-jNdfptanTI2-d7Hwm4SZE9hlhk'>Qt tricks [Google doc]</a><br>
<a href='law'>Law / <span lang='cs'>Zákony</span> [in czech]</a><br>
<a href='fireshow'>Fireshow</a><br>
<a href='android'>Android</a><br>
[Talks](talks)  

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.157.0/three.min.js" integrity="sha512-nogdM20cZX4FjsqU5H5ecK3vw8LjYN1AcUUWi7asLUVP3eJK5wldywvqFMW8CLd5/xoiJaIL3eXG82SlOWZkTA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script>
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
</script>
