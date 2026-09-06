from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "quickbite_secret_key"

DATABASE = "database.db"


# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    # FOOD TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            emoji TEXT NOT NULL
        )
    """)

    # ORDERS TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            total REAL,
            status TEXT DEFAULT 'New',
            created_at TEXT
        )
    """)

    # ADD FOOD
    count = conn.execute(
        "SELECT COUNT(*) FROM foods"
    ).fetchone()[0]

    if count == 0:

        foods = [
            ("Classic Burger", 149, "Burger", "🍔"),
            ("Cheese Pizza", 249, "Pizza", "🍕"),
            ("Chicken Biryani", 199, "Biryani", "🍗"),
            ("French Fries", 99, "Sides", "🍟"),
            ("Veg Momos", 129, "Snacks", "🥟"),
            ("Pasta", 179, "Pasta", "🍝"),
            ("Masala Dosa", 89, "Indian", "🥞"),
            ("Paneer Tikka", 189, "Indian", "🧀"),
            ("Chocolate Cake", 129, "Dessert", "🍰"),
            ("Cold Coffee", 99, "Drinks", "🥤")
        ]

        conn.executemany("""
            INSERT INTO foods
            (name, price, category, emoji)
            VALUES (?, ?, ?, ?)
        """, foods)

    conn.commit()
    conn.close()


# ================= HOME =================

@app.route("/")
def home():

    conn = get_db()

    foods = conn.execute(
        "SELECT * FROM foods LIMIT 6"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        foods=foods
    )


# ================= MENU =================

@app.route("/menu")
def menu():

    search = request.args.get("search", "").strip()
    craving = request.args.get("craving", "").strip().lower()

    conn = get_db()

    if search:

        foods = conn.execute("""
            SELECT * FROM foods
            WHERE name LIKE ?
            OR category LIKE ?
        """, (
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    else:

        foods = conn.execute(
            "SELECT * FROM foods"
        ).fetchall()

    # 🤖 AI CRAVING RECOMMENDATION

    craving_map = {

        "spicy": ["Biryani", "Indian", "Snacks"],

        "cheesy": ["Pizza", "Burger"],

        "sweet": ["Dessert"],

        "healthy": ["Indian", "Sides"],

        "crispy": ["Sides", "Snacks"],

        "comfort": ["Pasta", "Burger", "Biryani"],

        "drinks": ["Drinks"]
    }

    recommendations = []

    if craving in craving_map:

        categories = craving_map[craving]

        for food in foods:

            if food["category"] in categories:
                recommendations.append(food)

    conn.close()

    return render_template(
        "menu.html",
        foods=foods,
        search=search,
        craving=craving,
        recommendations=recommendations
    )

    # ================= SEARCH =================

    if search:

        foods = conn.execute("""
            SELECT * FROM foods
            WHERE name LIKE ?
            OR category LIKE ?
        """, (
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    else:

        foods = conn.execute(
            "SELECT * FROM foods"
        ).fetchall()

    # ================= AI RECOMMENDATION =================

    craving_map = {

        "spicy": [
            "Biryani",
            "Indian",
            "Snacks"
        ],

        "cheesy": [
            "Pizza",
            "Burger"
        ],

        "sweet": [
            "Dessert"
        ],

        "healthy": [
            "Indian",
            "Sides"
        ],

        "crispy": [
            "Sides",
            "Snacks"
        ],

        "comfort": [
            "Pasta",
            "Burger",
            "Biryani"
        ],

        "drinks": [
            "Drinks"
        ]
    }

    recommendations = []

    if craving in craving_map:

        categories = craving_map[craving]

        for food in foods:

            if food["category"] in categories:
                recommendations.append(food)

    # If nothing matches, show first 3 foods
    if craving and not recommendations:
        recommendations = foods[:3]

    conn.close()

    return render_template(
        "menu.html",
        foods=foods,
        search=search,
        craving=craving,
        recommendations=recommendations
    )


# ================= FOOD DETAILS =================

@app.route("/food/<int:food_id>")
def food_details(food_id):

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    conn.close()

    if food is None:
        return "Food not found", 404

    return render_template(
        "food.html",
        food=food
    )# ================= CUSTOMIZE MEAL =================

@app.route("/customize/<int:food_id>")
def customize(food_id):

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    conn.close()

    if food is None:
        return "Food not found", 404

    return render_template(
        "customization.html",
        food=food
    )
    # ================= ADD CUSTOMIZED MEAL =================

@app.route("/add_customized/<int:food_id>", methods=["POST"])
def add_customized(food_id):

    food = None

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    conn.close()

    if food is None:
        return "Food not found", 404

    spice_price = float(request.form.get("spice_price", 0))
    cheese_price = float(request.form.get("cheese_price", 0))
    toppings_price = float(request.form.get("toppings_price", 0))

    instructions = request.form.get(
        "instructions", ""
    ).strip()

    customized_price = (
        float(food["price"])
        + spice_price
        + cheese_price
        + toppings_price
    )

    cart = session.get("cart", {})

    food_id_str = str(food_id)

    if food_id_str in cart:
        cart[food_id_str] += 1
    else:
        cart[food_id_str] = 1

    session["cart"] = cart

    session["customization"] = {
        "food_id": food_id,
        "price": customized_price,
        "instructions": instructions
    }

    return redirect(url_for("cart"))


# ================= ADD TO CART =================

@app.route("/add/<int:food_id>")
def add_to_cart(food_id):

    cart = session.get("cart", {})

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    session["cart"] = cart

    return redirect(
        request.referrer or url_for("menu")
    )


# ================= REMOVE FROM CART =================

@app.route("/remove/<int:food_id>")
def remove_from_cart(food_id):

    cart = session.get("cart", {})

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] -= 1

        if cart[food_id] <= 0:
            del cart[food_id]

    session["cart"] = cart

    return redirect(url_for("cart"))


# ================= CART =================

@app.route("/cart")
def cart():

    cart = session.get("cart", {})

    items = []
    total = 0

    conn = get_db()

    customization = session.get("customization")

    for food_id, quantity in cart.items():

        food = conn.execute(
            "SELECT * FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            item_price = float(food["price"])

            # Apply customization to the customized food
            if (
                customization
                and str(customization.get("food_id")) == str(food_id)
            ):

                item_price = float(
                    customization.get("price", item_price)
                )

            subtotal = item_price * quantity

            items.append({
                "food": food,
                "quantity": quantity,
                "subtotal": subtotal,
                "item_price": item_price,
                "customization": (
                    customization
                    if (
                        customization
                        and str(customization.get("food_id"))
                        == str(food_id)
                    )
                    else None
                )
            })

            total += subtotal

    conn.close()

    discount = session.get("discount", 0)
    coupon = session.get("coupon", "")

    final_total = max(
        0,
        total - discount
    )

    return render_template(
        "cart.html",
        items=items,
        total=total,
        discount=discount,
        final_total=final_total,
        coupon=coupon
    )


# ================= COUPON =================

@app.route("/apply_coupon", methods=["POST"])
def apply_coupon():

    coupon = request.form.get("coupon", "").strip().upper()

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("cart"))

    # Calculate subtotal
    total = 0

    conn = get_db()

    for food_id, quantity in cart.items():

        food = conn.execute(
            "SELECT price FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:
            total += food["price"] * quantity

    conn.close()

    # Coupon rules
    if coupon == "WELCOME20":

        discount = total * 0.20

        session["discount"] = discount
        session["coupon"] = "WELCOME20"

    elif coupon == "FOOD50":

        discount = min(50, total)

        session["discount"] = discount
        session["coupon"] = "FOOD50"

    else:

        session["discount"] = 0
        session["coupon"] = ""

    return redirect(url_for("cart"))


# ================= CHECKOUT =================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("menu"))

    if request.method == "POST":

        session["customer"] = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "address": request.form["address"]
        }

        return redirect(url_for("payment"))

    return render_template("checkout.html")


# ================= PAYMENT =================

@app.route("/payment", methods=["GET", "POST"])
def payment():

    if "customer" not in session:
        return redirect(url_for("checkout"))

        cart = session.get("cart", {})

    total = 0

    conn = get_db()

    customization = session.get("customization")

    for food_id, quantity in cart.items():

        food = conn.execute(
            "SELECT * FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            item_price = float(food["price"])

            if (
                customization
                and str(customization.get("food_id"))
                == str(food_id)
            ):
                item_price = float(
                    customization.get("price", item_price)
                )

            total += item_price * quantity

    # Apply coupon discount
    discount = session.get("discount", 0)

    final_total = max(0, total - discount)

    if request.method == "POST":

        customer = session.get("customer", {})

        # SAVE ORDER FOR KITCHEN
        conn.execute("""
            INSERT INTO orders
            (customer_name, phone, address, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer.get("name"),
            customer.get("phone"),
            customer.get("address"),
            final_total,
            "New",
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        conn.close()

        # Clear cart
        session["cart"] = {}

        # Clear coupon
        session["discount"] = 0
        session["coupon"] = ""

        return redirect(url_for("success"))

    conn.close()

    return render_template(
        "payment.html",
        total=final_total
    )


# ================= SUCCESS =================

@app.route("/success")
def success():

    customer = session.get("customer", {})

    return render_template(
        "success.html",
        customer=customer
    )


# =====================================================
#                 SMART KITCHEN SYSTEM
# =====================================================


# ================= KITCHEN DASHBOARD =================

@app.route("/kitchen")
def kitchen():

    conn = get_db()

    orders = conn.execute("""
        SELECT * FROM orders
        ORDER BY id DESC
    """).fetchall()

    total_orders = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    preparing = conn.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Preparing'
    """).fetchone()[0]

    completed = conn.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Completed'
    """).fetchone()[0]

    ready = conn.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Ready'
    """).fetchone()[0]

    revenue = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM orders
    """).fetchone()[0]

    conn.close()

    return render_template(
        "kitchen.html",
        orders=orders,
        total_orders=total_orders,
        preparing=preparing,
        completed=completed,
        ready=ready,
        revenue=revenue
    )


# ================= UPDATE ORDER =================

@app.route("/kitchen/update/<int:order_id>/<status>")
def update_order_status(order_id, status):

    allowed_statuses = [
        "New",
        "Preparing",
        "Ready",
        "Completed"
    ]

    if status not in allowed_statuses:
        return redirect(url_for("kitchen"))

    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (
        status,
        order_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("kitchen"))


# ================= RUN =================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)