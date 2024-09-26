document.addEventListener('DOMContentLoaded', function () {
    const faqItems = document.querySelectorAll('.faq-item h4');

    faqItems.forEach(item => {
        item.addEventListener('click', function () {
            const parent = this.parentElement;
            parent.classList.toggle('expanded'); // Toggle the expanded class
            const answer = parent.querySelector('.faq-answer');

            // Toggle display of the answer
            if (answer.style.display === 'block') {
                answer.style.display = 'none';
            } else {
                answer.style.display = 'block';
            }

            // Rotate the arrow
            const arrow = this.querySelector('.faq-arrow');
            if (arrow) {
                arrow.classList.toggle('rotate');
            }
        });
    });
});
