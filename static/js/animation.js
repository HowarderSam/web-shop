document.addEventListener('DOMContentLoaded', () => {
    
    //clickable card
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const link = card.querySelector('a.btn');
        if (link) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', (e) => {
                if (!e.target.closest('button, a')) {
                    window.location.href = link.href;
                }
            });
        }
    });


    //navbar shadow 
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 30) {
                navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.08)';
            } else {
                navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
            }
        });
    }
});