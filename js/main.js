document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", function (event) {
        const section = document.querySelector(this.getAttribute("href"));

        if (section) {
            event.preventDefault();
            section.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});