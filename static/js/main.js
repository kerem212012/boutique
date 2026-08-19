document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.language-switcher select').forEach(function (languageSelect) {
        languageSelect.addEventListener('change', function () {
            languageSelect.form.submit();
        });
    });

    // Password toggle functionality
    document.querySelectorAll('.password-toggle').forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            
            if (passwordInput) {
                const isPassword = passwordInput.type === 'password';
                passwordInput.type = isPassword ? 'text' : 'password';
                
                // Toggle eye icon visibility
                const openEye = this.querySelector('.eye-icon');
                const closedEye = this.querySelector('.eye-closed-icon');
                if (openEye && closedEye) {
                    openEye.classList.toggle('hidden');
                    closedEye.classList.toggle('hidden');
                }
            }
        });
    });

    document.querySelectorAll('.conveyor-wrap').forEach(function (conveyor) {
        const cards = Array.from(conveyor.querySelectorAll('.card'));
        if (cards.length < 2) return;

        let current = 0;
        const delay = 2200;
        const duration = 700;
        let autoScrollTimer;
        let isAnimating = false;

        function easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }

        function smoothScrollTo(target, onComplete) {
            const start = conveyor.scrollLeft;
            const change = target - start;
            const startTime = performance.now();

            function animate(now) {
                const elapsed = Math.min((now - startTime) / duration, 1);
                const eased = easeInOutCubic(elapsed);
                conveyor.scrollLeft = start + change * eased;

                if (elapsed < 1) {
                    requestAnimationFrame(animate);
                } else if (onComplete) {
                    onComplete();
                }
            }

            requestAnimationFrame(animate);
        }

        function scrollToCard(index) {
            const left = cards[index].offsetLeft;
            isAnimating = true;
            smoothScrollTo(left, function () {
                current = index;
                isAnimating = false;
            });
        }

        function nextCard() {
            if (isAnimating) return;

            scrollToCard((current + 1) % cards.length);
        }

        autoScrollTimer = setInterval(nextCard, delay);

        conveyor.addEventListener('mouseenter', function () {
            clearInterval(autoScrollTimer);
        });

        conveyor.addEventListener('mouseleave', function () {
            clearInterval(autoScrollTimer);
            autoScrollTimer = setInterval(nextCard, delay);
        });
    });

    // Mobile language dropdown toggle
    const mobileLangToggle = document.querySelector('.mobile-lang-toggle');
    if (mobileLangToggle) {
        const mobileLang = mobileLangToggle.closest('.mobile-lang');
        const menu = mobileLang.querySelector('.mobile-lang-menu');

        mobileLangToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = mobileLang.classList.toggle('open');
            mobileLangToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            menu.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
        });

        document.addEventListener('click', function () {
            if (mobileLang.classList.contains('open')) {
                mobileLang.classList.remove('open');
                mobileLangToggle.setAttribute('aria-expanded', 'false');
                menu.setAttribute('aria-hidden', 'true');
            }
        });
    }

        // Mobile bottom menu (off-canvas)
        const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
        const mobileOffcanvas = document.querySelector('.mobile-offcanvas');
        if (mobileMenuToggle && mobileOffcanvas) {
            const openClass = 'open';
            function openMenu() {
                mobileOffcanvas.classList.add(openClass);
                mobileMenuToggle.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';
            }
            function closeMenu() {
                mobileOffcanvas.classList.remove(openClass);
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }

            mobileMenuToggle.addEventListener('click', function (e) {
                e.stopPropagation();
                if (mobileOffcanvas.classList.contains(openClass)) closeMenu(); else openMenu();
            });

            mobileOffcanvas.addEventListener('click', function (e) {
                if (e.target && e.target.dataset && e.target.dataset.action === 'close') {
                    closeMenu();
                }
            });
        }
});
