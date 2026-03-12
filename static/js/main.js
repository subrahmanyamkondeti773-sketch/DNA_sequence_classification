/**
 * DNA Classification System - Main JavaScript
 * Dark mode toggle, UI interactions, and AJAX helpers
 */

document.addEventListener('DOMContentLoaded', function () {

    // ===========================================
    // 1. DARK / LIGHT MODE TOGGLE
    // ===========================================
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    function applyTheme(theme) {
        htmlEl.setAttribute('data-bs-theme', theme);
        localStorage.setItem('dna-theme', theme);
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }
    }

    // Load saved theme
    const savedTheme = localStorage.getItem('dna-theme') || 'dark';
    applyTheme(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = htmlEl.getAttribute('data-bs-theme');
            applyTheme(current === 'dark' ? 'light' : 'dark');
        });
    }

    // ===========================================
    // 2. NAVBAR SCROLL EFFECT
    // ===========================================
    const navbar = document.getElementById('mainNav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.3)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }

    // ===========================================
    // 3. AUTO-DISMISS ALERTS
    // ===========================================
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // ===========================================
    // 4. ANIMATE STAT COUNTERS (Dashboard)
    // ===========================================
    function animateCounter(el, target) {
        const duration = 1500;
        const step = target / (duration / 16);
        let current = 0;
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.round(current).toLocaleString();
        }, 16);
    }

    document.querySelectorAll('.stat-card-value[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count, 10);
        if (!isNaN(target)) animateCounter(el, target);
    });

    // ===========================================
    // 5. CONFIDENCE BAR ANIMATIONS
    // ===========================================
    const confBars = document.querySelectorAll('.confidence-fill, .confidence-mini-bar');
    confBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = width; }, 200);
    });

    // ===========================================
    // 6. SEQUENCE BASE HOVER TOOLTIP
    // ===========================================
    const baseNames = { A: 'Adenine', T: 'Thymine', G: 'Guanine', C: 'Cytosine' };
    document.querySelectorAll('.dna-base').forEach(base => {
        const char = base.textContent.trim();
        if (baseNames[char]) {
            base.title = baseNames[char];
        }
    });

    // ===========================================
    // 7. FEATURE CARD ANIMATIONS (IntersectionObserver)
    // ===========================================
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.feature-card, .stat-card, .glass-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // ===========================================
    // 8. HERO CONFIDENCE BAR ANIMATION
    // ===========================================
    const demoBars = document.querySelectorAll('.confidence-bar-demo .confidence-fill');
    demoBars.forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = target; }, 800);
    });

    // ===========================================
    // 9. COPY SEQUENCE BUTTON (if present)
    // ===========================================
    const copyBtn = document.getElementById('copySequenceBtn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const seqEl = document.querySelector('.sequence-display');
            if (seqEl) {
                const text = seqEl.innerText.replace(/\s/g, '');
                navigator.clipboard.writeText(text).then(() => {
                    copyBtn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Copied!';
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy';
                    }, 2000);
                });
            }
        });
    }

});
