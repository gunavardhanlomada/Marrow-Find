document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript Loaded");

    setTimeout(() => {
        let alerts = document.querySelectorAll(".flash-messages");
        alerts.forEach(alert => alert.style.display = "none");
    }, 3000);
});
