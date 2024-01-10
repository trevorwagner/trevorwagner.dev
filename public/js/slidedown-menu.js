const hamburger = document.getElementById('hamburger');
const overlay = document.getElementById("overlay-menu");
let menuActive = false;

function toggleMenu() {
    overlay.classList.toggle('active');
    hamburger.classList.toggle('active');
    menuActive = !menuActive;
}

hamburger.addEventListener('click', () => {
    toggleMenu();
});

window.addEventListener('resize', () => {
    const vw = Math.max(
        document.documentElement.clientWidth || 0,
        window.innerWidth || 0
    );
    if (vw > 767 && menuActive) {
        toggleMenu();
    }
});