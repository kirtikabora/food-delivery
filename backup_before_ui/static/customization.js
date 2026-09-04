document.addEventListener("DOMContentLoaded", () => {

    const foodData =
        document.getElementById("foodData");

    if (!foodData) return;

    const basePrice =
        Number(foodData.dataset.price || 0);


    const totalPrice =
        document.getElementById("totalPrice");

    const spicePrice =
        document.getElementById("spicePrice");

    const cheesePrice =
        document.getElementById("cheesePrice");

    const toppingsPrice =
        document.getElementById("toppingsPrice");

    const instructions =
        document.getElementById("instructions");

    const instructionValue =
        document.getElementById("instructionValue");


    function calculateTotal() {

        let spice = 0;

        const selectedSpice =
            document.querySelector(
                'input[name="spice"]:checked'
            );

        if (selectedSpice) {
            spice =
                Number(selectedSpice.value);
        }


        let cheese = 0;

        const cheeseInput =
            document.getElementById("cheese");

        if (cheeseInput && cheeseInput.checked) {
            cheese =
                Number(cheeseInput.value);
        }


        let toppings = 0;

        document
            .querySelectorAll(".topping:checked")
            .forEach(item => {
                toppings += Number(item.value);
            });


        const total =
            basePrice +
            spice +
            cheese +
            toppings;


        totalPrice.textContent =
            total.toFixed(0);


        spicePrice.value = spice;

        cheesePrice.value = cheese;

        toppingsPrice.value = toppings;

    }


    document
        .querySelectorAll('input[name="spice"]')
        .forEach(input => {

            input.addEventListener(
                "change",
                calculateTotal
            );

        });


    const cheese =
        document.getElementById("cheese");

    if (cheese) {

        cheese.addEventListener(
            "change",
            calculateTotal
        );

    }


    document
        .querySelectorAll(".topping")
        .forEach(input => {

            input.addEventListener(
                "change",
                calculateTotal
            );

        });


    document
        .getElementById("customizationForm")
        .addEventListener("submit", () => {

            instructionValue.value =
                instructions.value;

        });


    calculateTotal();

});