from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
from reviews import reviews_bp


app = Flask(__name__)
app.secret_key = "quickbite_secret_key"

app.register_blueprint(reviews_bp)

DATABASE = "database.db"


# =====================================================
# DATABASE
# =====================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    # ================= FOOD TABLE =================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            emoji TEXT NOT NULL
        )
    """)

    # ================= ORDER TABLE =================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            total REAL,
            status TEXT DEFAULT 'New',
            created_at TEXT,
            priority INTEGER DEFAULT 1,
            prep_time INTEGER DEFAULT 15,
            rider_id INTEGER
        )
    """)

    # Fix older databases

    try:
        conn.execute("""
            ALTER TABLE orders
            ADD COLUMN priority INTEGER DEFAULT 1
        """)
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("""
            ALTER TABLE orders
            ADD COLUMN prep_time INTEGER DEFAULT 15
        """)
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("""
            ALTER TABLE orders
            ADD COLUMN rider_id INTEGER
        """)
    except sqlite3.OperationalError:
        pass

    # ================= RIDER TABLE =================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS riders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            status TEXT DEFAULT 'Available'
        )
    """)

    # ================= INVENTORY =================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            quantity INTEGER DEFAULT 0,
            minimum INTEGER DEFAULT 5
        )
    """)

    # ================= FOOD DATA =================

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

    # ================= RIDERS =================

    rider_count = conn.execute(
        "SELECT COUNT(*) FROM riders"
    ).fetchone()[0]

    if rider_count == 0:

        riders = [
            ("Rahul", "9876543210", "Available"),
            ("Arjun", "9876543211", "Available"),
            ("Aman", "9876543212", "Available"),
            ("Vikash", "9876543213", "Available")
        ]

        conn.executemany("""
            INSERT INTO riders
            (name, phone, status)
            VALUES (?, ?, ?)
        """, riders)

    # ================= INVENTORY =================

    inventory_count = conn.execute(
        "SELECT COUNT(*) FROM inventory"
    ).fetchone()[0]

    if inventory_count == 0:

        inventory = [
            ("Burger Buns", 20, 5),
            ("Cheese", 15, 5),
            ("Chicken", 20, 5),
            ("Pizza Base", 10, 3),
            ("Potatoes", 25, 5),
            ("Momos", 15, 5),
            ("Pasta", 20, 5),
            ("Paneer", 15, 5),
            ("Cake", 10, 3),
            ("Coffee", 20, 5)
        ]

        conn.executemany("""
            INSERT INTO inventory
            (item, quantity, minimum)
            VALUES (?, ?, ?)
        """, inventory)

    conn.commit()
    conn.close()


# =====================================================
# CART HELPERS
# =====================================================

def get_cart_item_count():

    normal_cart = session.get("cart", {})
    customized_cart = session.get("customized_cart", [])

    normal_count = sum(
        int(quantity)
        for quantity in normal_cart.values()
    )

    customized_count = len(customized_cart)

    return normal_count + customized_count


def get_cart_total():

    total = 0

    # -----------------------------
    # NORMAL CART
    # -----------------------------

    normal_cart = session.get("cart", {})

    conn = get_db()

    for food_id, quantity in normal_cart.items():

        food = conn.execute(
            "SELECT price FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:
            total += (
                float(food["price"])
                * int(quantity)
            )

    conn.close()

    # -----------------------------
    # CUSTOMIZED CART
    # -----------------------------

    customized_cart = session.get(
        "customized_cart",
        []
    )

    for item in customized_cart:

        total += float(
            item.get("price", 0)
        )

    # -----------------------------
    # DISCOUNT
    # -----------------------------

    discount = float(
        session.get("discount", 0)
    )

    return max(
        0,
        total - discount
    )


# =====================================================
# HOME
# =====================================================

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


# =====================================================
# MENU
# =====================================================

@app.route("/menu")
def menu():

    search = request.args.get(
        "search",
        ""
    )

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

    conn.close()

    return render_template(
        "menu.html",
        foods=foods,
        search=search
    )


# =====================================================
# FOOD DETAILS
# =====================================================

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
    )


# =====================================================
# NORMAL ADD TO CART
# =====================================================

@app.route("/add/<int:food_id>")
def add_to_cart(food_id):

    cart = session.get(
        "cart",
        {}
    )

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    session["cart"] = cart
    session.modified = True

    return redirect(
        request.referrer
        or url_for("menu")
    )


# =====================================================
# NORMAL REMOVE / DECREASE
# =====================================================

@app.route("/remove/<int:food_id>")
def remove_from_cart(food_id):

    cart = session.get(
        "cart",
        {}
    )

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] -= 1

        if cart[food_id] <= 0:
            del cart[food_id]

    session["cart"] = cart
    session.modified = True

    return redirect(
        url_for("cart")
    )


# =====================================================
# CUSTOMIZATION PAGE
# =====================================================

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


# =====================================================
# ADD CUSTOMIZED FOOD
# =====================================================

@app.route(
    "/add_customized/<int:food_id>",
    methods=["POST"]
)
def add_customized(food_id):

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    conn.close()

    if food is None:
        return "Food not found", 404

    base_price = float(
        food["price"]
    )

    spice_price = float(
        request.form.get(
            "spice_price",
            0
        )
    )

    cheese_price = float(
        request.form.get(
            "cheese_price",
            0
        )
    )

    toppings_price = float(
        request.form.get(
            "toppings_price",
            0
        )
    )

    instructions = request.form.get(
        "instructions",
        ""
    ).strip()

    final_price = (
        base_price
        + spice_price
        + cheese_price
        + toppings_price
    )

    customized_cart = session.get(
        "customized_cart",
        []
    )

    customized_cart.append({

        "food_id": food_id,

        "price": final_price,

        "spice_price": spice_price,

        "cheese_price": cheese_price,

        "toppings_price": toppings_price,

        "instructions": instructions

    })

    session["customized_cart"] = customized_cart

    session.modified = True

    return redirect(
        url_for("cart")
    )


# =====================================================
# REMOVE CUSTOMIZED FOOD
# =====================================================

@app.route(
    "/remove_customized/<int:index>"
)
def remove_customized(index):

    customized_cart = session.get(
        "customized_cart",
        []
    )

    if 0 <= index < len(customized_cart):

        customized_cart.pop(index)

    session["customized_cart"] = (
        customized_cart
    )

    session.modified = True

    return redirect(
        url_for("cart")
    )


# =====================================================
# CART
# =====================================================

@app.route("/cart")
def cart():

    normal_cart = session.get(
        "cart",
        {}
    )

    customized_cart = session.get(
        "customized_cart",
        []
    )

    items = []

    total = 0

    # =================================================
    # NORMAL ITEMS
    # =================================================

    conn = get_db()

    for food_id, quantity in normal_cart.items():

        food = conn.execute(
            "SELECT * FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            item_price = float(
                food["price"]
            )

            quantity = int(
                quantity
            )

            subtotal = (
                item_price
                * quantity
            )

            items.append({

                "food": food,

                "quantity": quantity,

                "item_price": item_price,

                "subtotal": subtotal,

                "customization": None,

                "custom_index": None,

                "is_customized": False

            })

            total += subtotal

    conn.close()

    # =================================================
    # CUSTOMIZED ITEMS
    # =================================================

    for index, custom in enumerate(
        customized_cart
    ):

        conn = get_db()

        food = conn.execute(
            "SELECT * FROM foods WHERE id = ?",
            (custom["food_id"],)
        ).fetchone()

        conn.close()

        if food:

            custom_price = float(
                custom.get(
                    "price",
                    food["price"]
                )
            )

            customization = {

                "instructions":
                    custom.get(
                        "instructions",
                        ""
                    ),

                "spice_price":
                    custom.get(
                        "spice_price",
                        0
                    ),

                "cheese_price":
                    custom.get(
                        "cheese_price",
                        0
                    ),

                "toppings_price":
                    custom.get(
                        "toppings_price",
                        0
                    )

            }

            items.append({

                "food": food,

                "quantity": 1,

                "item_price":
                    custom_price,

                "subtotal":
                    custom_price,

                "customization":
                    customization,

                "custom_index":
                    index,

                "is_customized":
                    True

            })

            total += custom_price

    # =================================================
    # COUPON
    # =================================================

    discount = float(
        session.get(
            "discount",
            0
        )
    )

    coupon = session.get(
        "coupon",
        ""
    )

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


# =====================================================
# COUPON
# =====================================================

@app.route(
    "/apply_coupon",
    methods=["POST"]
)
def apply_coupon():

    coupon = request.form.get(
        "coupon",
        ""
    ).strip().upper()

    if get_cart_item_count() == 0:

        session["discount"] = 0
        session["coupon"] = ""

        return redirect(
            url_for("cart")
        )

    # IMPORTANT:
    # Coupon is calculated on the
    # complete cart, including customized meals.

    normal_cart = session.get(
        "cart",
        {}
    )

    customized_cart = session.get(
        "customized_cart",
        []
    )

    total = 0

    conn = get_db()

    for food_id, quantity in normal_cart.items():

        food = conn.execute(
            "SELECT price FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

        if food:

            total += (
                float(food["price"])
                * int(quantity)
            )

    conn.close()

    for item in customized_cart:

        total += float(
            item.get("price", 0)
        )

    # -----------------------------
    # APPLY COUPON
    # -----------------------------

    if coupon == "WELCOME20":

        session["discount"] = (
            total * 0.20
        )

        session["coupon"] = (
            "WELCOME20"
        )

    elif coupon == "FOOD50":

        session["discount"] = min(
            50,
            total
        )

        session["coupon"] = (
            "FOOD50"
        )

    else:

        session["discount"] = 0

        session["coupon"] = ""

    session.modified = True

    return redirect(
        url_for("cart")
    )


# =====================================================
# CHECKOUT
# =====================================================

@app.route(
    "/checkout",
    methods=["GET", "POST"]
)
def checkout():

    if get_cart_item_count() == 0:

        return redirect(
            url_for("menu")
        )

    if request.method == "POST":

        session["customer"] = {

            "name": request.form.get(
                "name",
                ""
            ),

            "phone": request.form.get(
                "phone",
                ""
            ),

            "address": request.form.get(
                "address",
                ""
            )

        }

        session.modified = True

        return redirect(
            url_for("payment")
        )

    return render_template(
        "checkout.html"
    )


# =====================================================
# PAYMENT
# =====================================================

@app.route(
    "/payment",
    methods=["GET", "POST"]
)
def payment():

    if "customer" not in session:

        return redirect(
            url_for("checkout")
        )

    if get_cart_item_count() == 0:

        return redirect(
            url_for("menu")
        )

    final_total = get_cart_total()

    item_count = get_cart_item_count()

    # -----------------------------
    # SMART PRIORITY
    # -----------------------------

    if item_count >= 5:

        priority = 3

    elif item_count >= 3:

        priority = 2

    else:

        priority = 1

    # -----------------------------
    # PREPARATION TIME
    # -----------------------------

    prep_time = (
        10
        + (item_count * 5)
    )

    # -----------------------------
    # CREATE ORDER
    # -----------------------------

    if request.method == "POST":

        customer = session.get(
            "customer",
            {}
        )

        conn = get_db()

        conn.execute("""
            INSERT INTO orders
            (
                customer_name,
                phone,
                address,
                total,
                status,
                created_at,
                priority,
                prep_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            customer.get(
                "name",
                ""
            ),

            customer.get(
                "phone",
                ""
            ),

            customer.get(
                "address",
                ""
            ),

            final_total,

            "New",

            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

            priority,

            prep_time

        ))

        conn.commit()

        conn.close()

        # Clear ALL cart data

        session["cart"] = {}

        session["customized_cart"] = []

        session["discount"] = 0

        session["coupon"] = ""

        session.modified = True

        return redirect(
            url_for("success")
        )

    return render_template(
        "payment.html",
        total=final_total
    )


# =====================================================
# SUCCESS
# =====================================================

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


# =====================================================
# SMART KITCHEN
# =====================================================

@app.route("/kitchen")
def kitchen():

    conn = get_db()

    orders = conn.execute("""
        SELECT
            orders.*,
            riders.name AS rider_name
        FROM orders
        LEFT JOIN riders
        ON orders.rider_id = riders.id
        ORDER BY
            priority DESC,
            id DESC
    """).fetchall()

    total_orders = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    preparing = conn.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Preparing'
    """).fetchone()[0]

    ready = conn.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Ready'
    """).fetchone()[0]

    completed = conn.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Completed'
    """).fetchone()[0]

    revenue = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM orders
    """).fetchone()[0]

    riders = conn.execute(
        "SELECT * FROM riders"
    ).fetchall()

    inventory = conn.execute(
        "SELECT * FROM inventory"
    ).fetchall()

    conn.close()

    return render_template(
        "kitchen.html",

        orders=orders,

        total_orders=total_orders,

        preparing=preparing,

        ready=ready,

        completed=completed,

        revenue=revenue,

        riders=riders,

        inventory=inventory
    )


# =====================================================
# UPDATE ORDER STATUS
# =====================================================

@app.route(
    "/kitchen/update/<int:order_id>/<status>"
)
def update_order_status(
    order_id,
    status
):

    allowed_statuses = [
        "New",
        "Preparing",
        "Ready",
        "Completed"
    ]

    if status not in allowed_statuses:

        return redirect(
            url_for("kitchen")
        )

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

    return redirect(
        url_for("kitchen")
    )


# =====================================================
# ASSIGN RIDER
# =====================================================

@app.route(
    "/kitchen/assign/<int:order_id>",
    methods=["POST"]
)
def assign_rider(order_id):

    rider_id = request.form.get(
        "rider_id"
    )

    if not rider_id:

        return redirect(
            url_for("kitchen")
        )

    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET rider_id = ?
        WHERE id = ?
    """, (
        rider_id,
        order_id
    ))

    conn.execute("""
        UPDATE riders
        SET status = 'Busy'
        WHERE id = ?
    """, (
        rider_id,
    ))

    conn.commit()

    conn.close()

    return redirect(
        url_for("kitchen")
    )


# =====================================================
# RIDER AVAILABLE
# =====================================================

@app.route(
    "/kitchen/rider/<int:rider_id>/available"
)
def rider_available(rider_id):

    conn = get_db()

    conn.execute("""
        UPDATE riders
        SET status = 'Available'
        WHERE id = ?
    """, (
        rider_id,
    ))

    conn.commit()

    conn.close()

    return redirect(
        url_for("kitchen")
    )


# =====================================================
# INVENTORY
# =====================================================

@app.route(
    "/kitchen/inventory/<int:item_id>",
    methods=["POST"]
)
def update_inventory(item_id):

    quantity = request.form.get(
        "quantity",
        0
    )

    try:

        quantity = int(quantity)

    except ValueError:

        quantity = 0

    conn = get_db()

    conn.execute("""
        UPDATE inventory
        SET quantity = ?
        WHERE id = ?
    """, (
        quantity,
        item_id
    ))

    conn.commit()

    conn.close()

    return redirect(
        url_for("kitchen")
    )


# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )