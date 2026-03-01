document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('input-section');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loader = document.getElementById('loader');

    if (form) {
        form.addEventListener('submit', () => {
            analyzeBtn.style.display = 'none';
            loader.style.display = 'block';
        });
    }

    // Animation for result page (if on result page)
    const gaugeFill = document.querySelector('.gauge-fill');
    if (gaugeFill) {
        const finalWidth = gaugeFill.style.width;
        gaugeFill.style.width = '0%';
        setTimeout(() => {
            gaugeFill.style.width = finalWidth;
        }, 100);
    }
});
