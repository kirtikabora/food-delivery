console.log("QuickBite 🍔 is running!");

document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(".food-card");

    cards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            card.style.cursor = "pointer";
        });

    });

});