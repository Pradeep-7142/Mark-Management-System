// JavaScript for Bootstrap enhancements

document.addEventListener("DOMContentLoaded", function () {
    // Add smooth scrolling effect for buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function () {
            button.classList.add('active');
            setTimeout(() => button.classList.remove('active'), 150);
        });
    });
});
