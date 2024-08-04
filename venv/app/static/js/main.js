// app/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Add date picker to expiry date input
    const expiryDateInput = document.getElementById('expiry_date');
    if (expiryDateInput) {
        expiryDateInput.type = 'date';
    }

    // Confirm delete action
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this product?')) {
                event.preventDefault();
            }
        });
    });

    // Highlight expiring products
    const productRows = document.querySelectorAll('.product-row');
    const today = new Date();
    productRows.forEach(row => {
        const expiryDate = new Date(row.dataset.expiryDate);
        const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));
        
        if (daysUntilExpiry <= 3 && daysUntilExpiry > 0) {
            row.classList.add('expiring-soon');
        } else if (daysUntilExpiry <= 0) {
            row.classList.add('expired');
        }
    });
});

// app/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Fade-in animation
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('active');
        }, 100 * index);
    });

    // GSAP animations for cards
    gsap.from('.card', {
        duration: 0.8,
        opacity: 0,
        y: 50,
        stagger: 0.2,
        ease: 'power3.out'
    });

    // Highlight expiring products
    const productRows = document.querySelectorAll('.product-row');
    const today = new Date();
    productRows.forEach(row => {
        const expiryDate = new Date(row.dataset.expiryDate);
        const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));
        
        if (daysUntilExpiry <= 3 && daysUntilExpiry > 0) {
            row.classList.add('expiring-soon');
        } else if (daysUntilExpiry <= 0) {
            row.classList.add('expired');
        }
    });

    // Confirm delete action
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this product?')) {
                event.preventDefault();
            }
        });
    });
});

document.addEventListener('click', function(e) {
    if (e.target.closest('.delete-btn')) {
        e.preventDefault();
        if (confirm('Are you sure you want to delete this product?')) {
            window.location.href = e.target.closest('a').href;
        }
    }
});