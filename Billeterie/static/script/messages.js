document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg) {
        setTimeout(() => {
            msg.classList.add('hidden');
        }, 4000);
    });
});
