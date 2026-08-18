from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "quickbite_secret_key"

DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            emoji TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)

    # If old database exists without the new columns,
    # recreate the table.
    columns = conn.execute("PRAGMA table_info(foods)").fetchall()
    column_names = [column["name"] for column in columns]

    required = [
        "id",
        "name",
        "price",
        "category",
        "emoji",
        "description",
        "image"
    ]

    if not all(column in column_names for column in required):

        conn.execute("DROP TABLE IF EXISTS foods")

        conn.execute("""
            CREATE TABLE foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                emoji TEXT NOT NULL,
                description TEXT NOT NULL,
                image TEXT NOT NULL
            )
        """)

    count = conn.execute(
        "SELECT COUNT(*) FROM foods"
    ).fetchone()[0]

    if count == 0:

        foods = [

            (
                "Classic Burger",
                149,
                "Burger",
                "🍔",
                "Juicy grilled burger with fresh vegetables and special sauce.",
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Cheese Pizza",
                249,
                "Pizza",
                "🍕",
                "Hot cheesy pizza topped with fresh vegetables and herbs.",
                "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Chicken Biryani",
                199,
                "Biryani",
                "🍗",
                "Aromatic basmati rice cooked with tender chicken and spices.",
                "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "French Fries",
                99,
                "Sides",
                "🍟",
                "Crispy golden fries served hot and perfectly seasoned.",
                "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Veg Momos",
                129,
                "Snacks",
                "🥟",
                "Soft steamed dumplings filled with delicious vegetables.",
                "https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Creamy Pasta",
                179,
                "Pasta",
                "🍝",
                "Creamy Italian pasta with herbs and parmesan.",
                "https://images.unsplash.com/photo-1551892374-ecf8754cf8b0?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Masala Dosa",
                89,
                "Indian",
                "🥞",
                "Crispy dosa served with flavorful potato masala.",
                "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Paneer Tikka",
                189,
                "Indian",
                "🧀",
                "Grilled paneer marinated with Indian spices.",
                "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Chocolate Cake",
                129,
                "Dessert",
                "🍰",
                "Rich chocolate cake with a soft and creamy texture.",
                "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=85"
            ),

            (
                "Cold Coffee",
                99,
                "Drinks",
                "🥤",
                "Chilled creamy coffee perfect for a refreshing break.",
                "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=85"
            )
        ]

        conn.executemany("""
            INSERT INTO foods
            (name, price, category, emoji, description, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, foods)

    conn.commit()
    conn.close()


# =========================
# HOME
# =========================

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


# =========================
# MENU
# =========================

@app.route("/menu")
def menu():

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    conn = get_db()

    query = "SELECT * FROM foods WHERE 1=1"
    params = []

    if search:

        query += """
            AND (
                name LIKE ?
                OR category LIKE ?
            )
        """

        params.extend([
            f"%{search}%",
            f"%{search}%"
        ])

    if category:

        query += " AND category = ?"

        params.append(category)

    foods = conn.execute(
        query,
        params
    ).fetchall()

    categories = conn.execute(
        "SELECT DISTINCT category FROM foods"
    ).fetchall()

    conn.close()

    return render_template(
        "menu.html",
        foods=foods,
        search=search,
        category=category,
        categories=categories
    )


# =========================
# FOOD DETAILS
# =========================

@app.route("/food/<int:food_id>")
def food_details(food_id):

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    conn.close()

    if not food:
        return "Food not found", 404

    return render_template(
        "food.html",
        food=food
    )


# =========================
# ADD TO CART
# =========================

@app.route("/add/<int:food_id>")
def add_to_cart(food_id):

    cart = session.get("cart", {})

    food_id = str(food_id)

    cart[food_id] = cart.get(food_id, 0) + 1

    session["cart"] = cart

    return redirect(
        request.referrer or url_for("menu")
    )


# =========================
# REMOVE FROM CART
# =========================

@app.route("/remove/<int:food_id>")
def remove_from_cart(food_id):

    cart = session.get("cart", {})

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] -= 1

        if cart[food_id] <= 0:
            del cart[food_id]

    session["cart"] = cart

    return redirect(
        url_for("cart")
    )


# =========================
# CART
# =========================

@app.route("/cart")
def cart():

    cart = session.get("cart", {})

    items = []

    total = 0

    conn = get_db()

    for food_id, quantity in cart.items():

        food = conn.execute(
            "SELECT * FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            subtotal = food["price"] * quantity

            items.append({
                "food": food,
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    conn.close()

    discount = session.get(
        "discount",
        0
    )

    coupon = session.get(
        "coupon",
        ""
    )

    final_total = max(
        total - discount,
        0
    )

    return render_template(
        "cart.html",
        items=items,
        total=total,
        discount=discount,
        final_total=final_total,
        coupon=coupon
    )


# =========================
# COUPON
# =========================

@app.route(
    "/apply_coupon",
    methods=["POST"]
)
def apply_coupon():

    code = request.form.get(
        "coupon",
        ""
    ).upper().strip()

    cart = session.get(
        "cart",
        {}
    )

    if not cart:
        return redirect(
            url_for("cart")
        )

    conn = get_db()

    total = 0

    for food_id, quantity in cart.items():

        food = conn.execute(
            "SELECT price FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            total += (
                food["price"] *
                quantity
            )

    conn.close()

    if code == "WELCOME20":

        discount = total * 0.20

        session["discount"] = discount
        session["coupon"] = code

    elif code == "FOOD50":

        discount = min(
            50,
            total
        )

        session["discount"] = discount
        session["coupon"] = code

    else:

        session["discount"] = 0
        session["coupon"] = ""

    return redirect(
        url_for("cart")
    )


# =========================
# CHECKOUT
# =========================

@app.route(
    "/checkout",
    methods=["GET", "POST"]
)
def checkout():

    cart = session.get(
        "cart",
        {}
    )

    if not cart:

        return redirect(
            url_for("menu")
        )

    if request.method == "POST":

        session["customer"] = {

            "name":
                request.form["name"],

            "phone":
                request.form["phone"],

            "address":
                request.form["address"]
        }

        return redirect(
            url_for("payment")
        )

    return render_template(
        "checkout.html"
    )


# =========================
# PAYMENT
# =========================

@app.route(
    "/payment",
    methods=["GET", "POST"]
)
def payment():

    if "customer" not in session:

        return redirect(
            url_for("checkout")
        )

    cart = session.get(
        "cart",
        {}
    )

    total = 0

    conn = get_db()

    for food_id, quantity in cart.items():

        food = conn.execute(
            "SELECT price FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            total += (
                food["price"] *
                quantity
            )

    conn.close()

    discount = session.get(
        "discount",
        0
    )

    final_total = max(
        total - discount,
        0
    )

    if request.method == "POST":

        session["order_status"] = (
            "Order Placed"
        )

        session["cart"] = {}

        session["discount"] = 0

        session["coupon"] = ""

        return redirect(
            url_for("success")
        )

    return render_template(
        "payment.html",
        total=final_total
    )


# =========================
# SUCCESS / TRACKING
# =========================

@app.route("/success")
def success():

    customer = session.get(
        "customer",
        {}
    )

    return render_template(
        "success.html",
        customer=customer
    )


# =========================
# START APP
# =========================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )