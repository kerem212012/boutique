document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.language-switcher select').forEach(function (languageSelect) {
        languageSelect.addEventListener('change', function () {
            languageSelect.form.submit();
        });
    });

    document.querySelectorAll('.conveyor-wrap').forEach(function (conveyor) {
        const cards = Array.from(conveyor.querySelectorAll('.card'));
        if (!cards.length) return;

        const originalCardCount = Math.floor(cards.length / 3);
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

                if (current >= originalCardCount) {
                    conveyor.scrollLeft = cards[current - originalCardCount].offsetLeft;
                    current -= originalCardCount;
                }
            });
        }

        function nextCard() {
            if (isAnimating) return;

            scrollToCard(current + 1);
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
});