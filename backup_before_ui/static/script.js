/* =========================================================
   QUICKBITE — MODERN FOOD DELIVERY UI
   ========================================================= */

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --orange: #ff5a36;
    --orange-dark: #e94725;
    --orange-light: #fff1eb;
    --cream: #fffaf7;
    --dark: #171717;
    --text: #292929;
    --muted: #777;
    --white: #ffffff;
    --green: #20a464;
    --border: #eeeeee;
    --shadow: 0 12px 35px rgba(20, 20, 20, 0.08);
    --shadow-hover: 0 20px 50px rgba(20, 20, 20, 0.13);
    --radius: 20px;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: "DM Sans", Arial, sans-serif;
    background: var(--cream);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}

/* =========================================================
   NAVBAR
   ========================================================= */

nav {
    height: 76px;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6%;
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.logo {
    text-decoration: none;
    color: var(--dark);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.logo span {
    color: var(--orange);
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-links a {
    text-decoration: none;
    color: #555;
    font-weight: 600;
    padding: 10px 15px;
    border-radius: 12px;
    transition: 0.25s ease;
}

.nav-links a:hover {
    color: var(--orange);
    background: var(--orange-light);
}

.cart-link {
    position: relative;
    padding-right: 17px !important;
}

.cart-badge {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 20px;
    height: 20px;
    padding: 0 5px;
    border-radius: 50px;
    background: var(--orange);
    color: white;
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid white;
    transform: scale(0);
    transition: transform 0.25s ease;
}

.cart-badge.show {
    transform: scale(1);
}

.cart-badge.bump {
    animation: badgeBump 0.45s ease;
}

@keyframes badgeBump {
    0% { transform: scale(1); }
    45% { transform: scale(1.35); }
    100% { transform: scale(1); }
}

/* =========================================================
   BUTTONS
   ========================================================= */

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    background: var(--orange);
    color: white;
    padding: 13px 21px;
    border-radius: 13px;
    font-family: inherit;
    font-weight: 700;
    font-size: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease,
                background 0.2s ease;
    position: relative;
    overflow: hidden;
}

.btn:hover {
    background: var(--orange-dark);
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(255, 90, 54, 0.25);
}

.btn:active {
    transform: scale(0.97);
}

.btn-outline {
    background: white;
    color: var(--orange);
    border: 1px solid #ffd3c7;
}

.btn-outline:hover {
    background: var(--orange-light);
    color: var(--orange-dark);
}

.btn-dark {
    background: var(--dark);
}

.btn-dark:hover {
    background: #333;
}

/* =========================================================
   RIPPLE
   ========================================================= */

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.45);
    transform: scale(0);
    animation: ripple 0.55s linear;
    pointer-events: none;
}

@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

/* =========================================================
   PAGE ANIMATION
   ========================================================= */

body {
    animation: pageIn 0.45s ease;
}

@keyframes pageIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.page-exit {
    animation: pageOut 0.2s ease forwards;
}

@keyframes pageOut {
    to {
        opacity: 0;
        transform: translateY(-5px);
    }
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    width: 88%;
    max-width: 1320px;
    min-height: 620px;
    margin: 35px auto 0;
    border-radius: 34px;
    padding: 70px 7%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 60px;
    overflow: hidden;
    background:
        radial-gradient(circle at 80% 20%, rgba(255,255,255,0.8), transparent 30%),
        linear-gradient(135deg, #fff0e9, #ffe1d4);
}

.hero-content {
    max-width: 590px;
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: white;
    color: var(--orange);
    padding: 9px 14px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 800;
    box-shadow: 0 7px 20px rgba(0,0,0,0.05);
}

.hero h1 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(45px, 6vw, 72px);
    line-height: 1.02;
    letter-spacing: -3px;
    margin: 25px 0 20px;
    color: var(--dark);
}

.hero h1 span {
    color: var(--orange);
}

.hero p {
    color: #686868;
    font-size: 18px;
    max-width: 520px;
    margin-bottom: 30px;
}

.hero-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.hero-image {
    width: min(430px, 42vw);
    height: min(430px, 42vw);
    min-width: 300px;
    min-height: 300px;
    border-radius: 50%;
    overflow: hidden;
    border: 12px solid rgba(255,255,255,0.7);
    box-shadow: 0 30px 70px rgba(190, 75, 35, 0.18);
    animation: heroFloat 5s ease-in-out infinite;
}

.hero-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

@keyframes heroFloat {
    0%, 100% {
        transform: translateY(0) rotate(0);
    }

    50% {
        transform: translateY(-12px) rotate(1deg);
    }
}

/* =========================================================
   CONTAINERS
   ========================================================= */

.container {
    width: 88%;
    max-width: 1320px;
    margin: 85px auto;
}

.section-heading {
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 20px;
    margin-bottom: 30px;
}

.section-heading h2 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(27px, 4vw, 38px);
    letter-spacing: -1.5px;
}

.section-heading a {
    color: var(--orange);
    text-decoration: none;
    font-weight: 700;
}

.mini-title {
    color: var(--orange);
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* =========================================================
   FOOD CARDS
   ========================================================= */

.food-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 26px;
}

.food-card-link {
    color: inherit;
    text-decoration: none;
}

.food-card {
    background: white;
    border: 1px solid rgba(0,0,0,0.04);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: 0.35s ease;
}

.food-card:hover {
    transform: translateY(-9px);
    box-shadow: var(--shadow-hover);
}

.food-photo {
    height: 235px;
    position: relative;
    overflow: hidden;
    background: #eee;
}

.food-photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.55s ease;
}

.food-card:hover .food-photo img {
    transform: scale(1.08);
}

.food-emoji {
    position: absolute;
    right: 15px;
    bottom: 15px;
    background: rgba(255,255,255,0.94);
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 21px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.food-info {
    padding: 21px;
}

.category {
    color: var(--orange);
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.food-info h3 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 19px;
    margin: 6px 0;
}

.food-info p {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.55;
    margin-bottom: 18px;
}

.food-bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.food-bottom strong {
    font-size: 20px;
}

.view-food {
    color: var(--orange);
    font-weight: 800;
    font-size: 14px;
}

/* =========================================================
   MENU
   ========================================================= */

.menu-header {
    padding: 70px 8%;
    background:
        radial-gradient(circle at 85% 20%, rgba(255,255,255,.8), transparent 25%),
        linear-gradient(135deg, #fff1ea, #ffe3d7);
}

.menu-header h1 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(38px, 5vw, 58px);
    letter-spacing: -2px;
    margin: 12px 0;
}

.menu-header p {
    color: #666;
    font-size: 17px;
}

.big-search {
    background: white;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 7px;
    display: flex;
    align-items: center;
    box-shadow: var(--shadow);
    margin-bottom: 25px;
}

.big-search span {
    padding: 0 15px;
    font-size: 20px;
}

.big-search input {
    flex: 1;
    border: none;
    outline: none;
    padding: 14px;
    font: inherit;
    font-size: 15px;
}

.big-search button {
    border: none;
    background: var(--orange);
    color: white;
    padding: 13px 23px;
    border-radius: 11px;
    cursor: pointer;
    font: inherit;
    font-weight: 800;
}

.categories {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 27px;
}

.category-btn {
    text-decoration: none;
    color: #555;
    background: white;
    border: 1px solid var(--border);
    padding: 10px 17px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 14px;
    transition: 0.25s;
}

.category-btn:hover,
.category-btn.selected {
    color: white;
    background: var(--orange);
    border-color: var(--orange);
    transform: translateY(-2px);
}

.menu-count {
    color: var(--muted);
    margin-bottom: 25px;
}

/* =========================================================
   FOOD DETAILS
   ========================================================= */

.food-detail-container {
    width: 88%;
    max-width: 1250px;
    margin: 55px auto;
}

.back-link {
    color: var(--orange);
    text-decoration: none;
    font-weight: 800;
}

.food-detail {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 65px;
    margin-top: 28px;
    align-items: center;
}

.detail-image {
    height: 540px;
    border-radius: 30px;
    overflow: hidden;
    box-shadow: var(--shadow-hover);
}

.detail-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.detail-info h1 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(38px, 5vw, 57px);
    line-height: 1.05;
    letter-spacing: -2px;
    margin: 12px 0;
}

.rating {
    color: #f2a900;
    font-size: 18px;
    margin: 18px 0;
}

.rating span {
    color: var(--muted);
    font-size: 14px;
}

.detail-description {
    color: #666;
    font-size: 16px;
    line-height: 1.8;
}

.detail-price {
    font-size: 35px;
    font-weight: 800;
    color: var(--orange);
    margin: 23px 0;
}

.detail-info-box {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 25px;
}

.detail-info-box div {
    background: white;
    border: 1px solid var(--border);
    padding: 11px 14px;
    border-radius: 13px;
    font-size: 13px;
    font-weight: 600;
}

.add-big {
    width: 100%;
    font-size: 16px;
    padding: 15px;
    margin-top: 8px;
}

/* =========================================================
   CART
   ========================================================= */

.cart-page {
    width: 88%;
    max-width: 1250px;
    margin: 55px auto;
}

.cart-page h1 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 42px;
    letter-spacing: -1.5px;
    margin-bottom: 30px;
}

.cart-layout {
    display: grid;
    grid-template-columns: 1.5fr 0.8fr;
    gap: 25px;
}

.cart-container {
    background: white;
    padding: 28px;
    border-radius: 22px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
}

.cart-item {
    display: grid;
    grid-template-columns: 1fr 150px 100px;
    align-items: center;
    gap: 20px;
    padding: 19px 0;
    border-bottom: 1px solid #f0f0f0;
}

.cart-item:last-child {
    border-bottom: none;
}

.cart-food {
    display: flex;
    align-items: center;
    gap: 15px;
}

.cart-image {
    width: 82px;
    height: 72px;
    border-radius: 13px;
    object-fit: cover;
}

.cart-food h3 {
    font-size: 16px;
    margin-bottom: 3px;
}

.cart-food small {
    color: var(--muted);
}

.quantity {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 11px;
}

.quantity a {
    width: 31px;
    height: 31px;
    display: grid;
    place-items: center;
    background: var(--orange);
    color: white;
    text-decoration: none;
    border-radius: 50%;
    font-weight: 800;
    transition: .2s;
}

.quantity a:hover {
    transform: scale(1.1);
}

.cart-price {
    text-align: right;
    font-weight: 800;
}

.customization-note {
    color: var(--orange);
    font-size: 13px;
    margin-top: 4px;
}

/* =========================================================
   COUPON / BILL
   ========================================================= */

.coupon {
    margin-top: 25px;
    padding: 19px;
    background: var(--orange-light);
    border-radius: 16px;
}

.coupon h3 {
    margin-bottom: 4px;
}

.coupon form {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}

.coupon input {
    flex: 1;
    border: 1px solid #ffd5ca;
    border-radius: 11px;
    padding: 12px;
    outline: none;
    font: inherit;
}

.coupon button {
    border: none;
    background: var(--orange);
    color: white;
    border-radius: 11px;
    padding: 12px 18px;
    font-weight: 800;
    cursor: pointer;
}

.coupon-success {
    color: var(--green);
    font-size: 13px;
    margin-top: 8px;
}

.bill {
    background: white;
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px;
    box-shadow: var(--shadow);
    height: fit-content;
    position: sticky;
    top: 100px;
}

.bill h2 {
    font-family: "Plus Jakarta Sans", sans-serif;
    margin-bottom: 22px;
}

.bill-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 13px;
    color: #666;
}

.bill-total {
    border-top: 1px dashed #ddd;
    padding-top: 17px;
    margin-top: 15px;
    display: flex;
    justify-content: space-between;
    font-size: 21px;
    font-weight: 800;
}

.discount {
    color: var(--green) !important;
}

.checkout-btn {
    width: 100%;
    margin-top: 22px;
}

/* =========================================================
   FORMS
   ========================================================= */

.form-container {
    width: 90%;
    max-width: 650px;
    margin: 65px auto;
    background: white;
    padding: 35px;
    border-radius: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}

.form-container h1 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 34px;
    margin-bottom: 8px;
}

.form-container p {
    color: var(--muted);
    margin-bottom: 25px;
}

.form-container form {
    display: flex;
    flex-direction: column;
    gap: 9px;
}

.form-container label {
    font-weight: 700;
    margin-top: 10px;
}

.form-container input,
.form-container textarea,
.form-container select {
    width: 100%;
    padding: 14px;
    border: 1px solid #ddd;
    border-radius: 12px;
    font: inherit;
    outline: none;
    transition: .2s;
}

.form-container input:focus,
.form-container textarea:focus,
.form-container select:focus {
    border-color: var(--orange);
    box-shadow: 0 0 0 4px rgba(255,90,54,.08);
}

/* =========================================================
   SUCCESS
   ========================================================= */

.success-container {
    width: 90%;
    max-width: 850px;
    margin: 70px auto;
    text-align: center;
}

.success-icon {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    margin: 0 auto 20px;
    display: grid;
    place-items: center;
    background: #e9f9f0;
    font-size: 45px;
    animation: successPop .65s cubic-bezier(.2,.9,.3,1.4);
}

@keyframes successPop {
    0% {
        transform: scale(0);
    }
    70% {
        transform: scale(1.12);
    }
    100% {
        transform: scale(1);
    }
}

.success-container h1 {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 42px;
    letter-spacing: -1.5px;
}

.success-container > p {
    color: var(--muted);
    margin: 10px 0 35px;
}

.tracking {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: var(--shadow);
    margin-bottom: 25px;
}

.track-step {
    text-align: center;
    flex: 1;
}

.track-icon {
    width: 45px;
    height: 45px;
    display: grid;
    place-items: center;
    background: var(--orange-light);
    border-radius: 50%;
    margin: auto;
}

.track-step.active .track-icon {
    background: var(--orange);
    color: white;
}

.track-step small {
    display: block;
    margin-top: 8px;
    font-weight: 700;
}

.track-line {
    height: 3px;
    flex: .5;
    background: #ddd;
}

.track-line.active {
    background: var(--orange);
}

.delivery-card {
    background: var(--dark);
    color: white;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
}

/* =========================================================
   EMPTY
   ========================================================= */

.empty {
    text-align: center;
    padding: 80px 30px;
    background: white;
    border-radius: 22px;
    box-shadow: var(--shadow);
}

.empty-icon {
    font-size: 55px;
    margin-bottom: 10px;
}

.empty h2 {
    font-family: "Plus Jakarta Sans", sans-serif;
}

/* =========================================================
   FOOTER
   ========================================================= */

footer {
    margin-top: 100px;
    padding: 45px 20px;
    background: #171717;
    color: white;
    text-align: center;
}

footer strong {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 20px;
}

footer p {
    color: #999;
    margin-top: 7px;
}

/* =========================================================
   TOAST
   ========================================================= */

.quickbite-toast {
    position: fixed;
    right: 25px;
    bottom: 25px;
    z-index: 9999;
    background: #171717;
    color: white;
    padding: 14px 19px;
    border-radius: 14px;
    box-shadow: 0 15px 40px rgba(0,0,0,.2);
    font-weight: 700;
    transform: translateY(25px);
    opacity: 0;
    pointer-events: none;
    transition: .3s ease;
}

.quickbite-toast.show {
    transform: translateY(0);
    opacity: 1;
}

/* =========================================================
   FLY TO CART
   ========================================================= */

.flying-food {
    position: fixed;
    z-index: 99999;
    pointer-events: none;
    width: 65px;
    height: 65px;
    object-fit: cover;
    border-radius: 50%;
    box-shadow: 0 12px 30px rgba(0,0,0,.25);
    transition: all .55s cubic-bezier(.2,.8,.3,1);
}

/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 950px) {

    .hero {
        flex-direction: column;
        text-align: center;
        padding: 55px 7%;
    }

    .hero-content {
        max-width: 700px;
    }

    .hero p {
        margin-left: auto;
        margin-right: auto;
    }

    .hero-actions {
        justify-content: center;
    }

    .food-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .food-detail {
        grid-template-columns: 1fr;
    }

    .detail-image {
        height: 430px;
    }

    .cart-layout {
        grid-template-columns: 1fr;
    }

    .bill {
        position: static;
    }
}

@media (max-width: 650px) {

    nav {
        padding: 0 4%;
    }

    .logo {
        font-size: 19px;
    }

    .nav-links {
        gap: 2px;
    }

    .nav-links a {
        padding: 8px;
        font-size: 13px;
    }

    .nav-links a span {
        display: none;
    }

    .hero {
        width: 94%;
        margin-top: 15px;
        min-height: auto;
        border-radius: 25px;
    }

    .hero h1 {
        letter-spacing: -2px;
    }

    .hero-image {
        width: 280px;
        height: 280px;
        min-width: 280px;
        min-height: 280px;
    }

    .container,
    .food-detail-container,
    .cart-page {
        width: 92%;
    }

    .food-grid {
        grid-template-columns: 1fr;
    }

    .section-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .menu-header {
        padding: 50px 5%;
    }

    .big-search {
        flex-wrap: wrap;
    }

    .big-search input {
        min-width: 150px;
    }

    .big-search button {
        width: 100%;
    }

    .cart-item {
        grid-template-columns: 1fr;
        gap: 12px;
    }

    .cart-price {
        text-align: left;
    }

    .quantity {
        justify-content: flex-start;
    }

    .tracking {
        flex-direction: column;
        gap: 15px;
    }

    .track-line {
        width: 3px;
        height: 30px;
        flex: none;
    }

    .form-container {
        padding: 25px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
    }
}