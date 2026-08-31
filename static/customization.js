const foodData = document.getElementById("foodData");

const basePrice = Number(
    foodData.dataset.price
);

const spiceOptions = document.querySelectorAll(
    'input[name="spice"]'
);

const cheese = document.getElementById("cheese");

const toppings = document.querySelectorAll(
    ".topping"
);

const totalPrice = document.getElementById(
    "totalPrice"
);


// Calculate total price
function calculatePrice() {

    let total = basePrice;

    // Spice price
    const selectedSpice = document.querySelector(
        'input[name="spice"]:checked'
    );

    if (selectedSpice) {
        total += Number(selectedSpice.value);
    }

    // Cheese price
    if (cheese.checked) {
        total += Number(cheese.value);
    }

    // Toppings price
    toppings.forEach(function(topping) {

        if (topping.checked) {
            total += Number(topping.value);
        }

    });

    // Show total price
    totalPrice.textContent = total;
}


// When spice is changed
spiceOptions.forEach(function(option) {

    option.addEventListener(
        "change",
        calculatePrice
    );

});


// When cheese is selected/unselected
cheese.addEventListener(
    "change",
    calculatePrice
);


// When toppings are selected/unselected
toppings.forEach(function(topping) {

    topping.addEventListener(
        "change",
        calculatePrice
    );

});


// Add customized meal to cart
document.getElementById("customizationForm")
    .addEventListener("submit", function() {

        const selectedSpice =
            document.querySelector(
                'input[name="spice"]:checked'
            );

        document.getElementById("spicePrice").value =
            selectedSpice
                ? selectedSpice.value
                : 0;

        document.getElementById("cheesePrice").value =
            cheese.checked
                ? cheese.value
                : 0;

        let toppingsTotal = 0;

        toppings.forEach(function(topping) {
            if (topping.checked) {
                toppingsTotal += Number(topping.value);
            }
        });

        document.getElementById("toppingsPrice").value =
            toppingsTotal;

        document.getElementById("instructionValue").value =
            document.getElementById("instructions").value;
    });


// Initial price calculation
calculatePrice();