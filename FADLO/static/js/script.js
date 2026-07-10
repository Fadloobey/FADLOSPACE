// ============================================================
// FADLO – Animated Frontend (v9)
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ---- Scroll Progress Bar ----
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = (scrollTop / docHeight) * 100;
            progressBar.style.width = progress + '%';
        });
    }

    // ---- Back to Top Button ----
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ---- Typewriter Effect (if present) ----
    const typedElement = document.getElementById('typed-text');
    if (typedElement) {
        const strings = typedElement.dataset.strings ? JSON.parse(typedElement.dataset.strings) : [
            'Welcome to FADLO',
            'Your Digital Platform',
            'Built with ❤️'
        ];
        let stringIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let currentText = '';

        function type() {
            const fullText = strings[stringIndex];
            if (isDeleting) {
                currentText = fullText.substring(0, charIndex - 1);
                charIndex--;
            } else {
                currentText = fullText.substring(0, charIndex + 1);
                charIndex++;
            }
            typedElement.textContent = currentText;
            if (!isDeleting && charIndex === fullText.length) {
                isDeleting = true;
                setTimeout(type, 1500);
                return;
            }
            if (isDeleting && charIndex === 0) {
                isDeleting = false;
                stringIndex = (stringIndex + 1) % strings.length;
                setTimeout(type, 300);
                return;
            }
            const speed = isDeleting ? 50 : 80;
            setTimeout(type, speed);
        }
        type();
    }

    // ---- Animate counters (already in index.html, but we re-run for safety) ----
    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-target'));
                let current = 0;
                const increment = Math.ceil(target / 80);
                const update = () => {
                    current += increment;
                    if (current >= target) {
                        el.textContent = target;
                        return;
                    }
                    el.textContent = current;
                    setTimeout(update, 20);
                };
                update();
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    counters.forEach(c => observer.observe(c));

    // ---- Staggered AOS (if AOS is present) ----
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: false,
            mirror: true,
            offset: 50,
            easing: 'ease-out-cubic',
        });
    }

    // ---- Sidebar toggle (handled in base.html, but we ensure it works) ----
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }

    // ---- Notification badge update (already in base.html) ----
    // kept for reference, not needed here.
});