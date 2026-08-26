import sqlite3
from flask import Blueprint, request, jsonify, redirect, url_for

reviews_bp = Blueprint("reviews", __name__)

DATABASE = "database.db"


def get_reviews_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_reviews_table():
    conn = get_reviews_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_reviews_table()


@reviews_bp.route("/reviews/<int:food_id>", methods=["POST"])
def submit_review(food_id):

    rating = request.form.get("rating")
    comment = request.form.get("comment", "").strip()

    # Check rating
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return "Invalid rating", 400

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5", 400

    # Check comment
    if not comment:
        return "Review comment cannot be empty", 400

    conn = get_reviews_db()

    # Check that food exists
    food = conn.execute(
        "SELECT id FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    if food is None:
        conn.close()
        return "Food not found", 404

    # Save review
    conn.execute("""
        INSERT INTO reviews (food_id, rating, comment)
        VALUES (?, ?, ?)
    """, (
        food_id,
        rating,
        comment
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("food_details", food_id=food_id))


@reviews_bp.route("/reviews/api/<int:food_id>")
def get_food_reviews(food_id):

    conn = get_reviews_db()

    reviews = conn.execute("""
        SELECT id, food_id, rating, comment
        FROM reviews
        WHERE food_id = ?
        ORDER BY id DESC
    """, (
        food_id,
    )).fetchall()

    result = conn.execute("""
        SELECT
            AVG(rating) AS average_rating,
            COUNT(*) AS review_count
        FROM reviews
        WHERE food_id = ?
    """, (
        food_id,
    )).fetchone()

    conn.close()

    average_rating = result["average_rating"]

    if average_rating is not None:
        average_rating = round(average_rating, 1)
    else:
        average_rating = 0

    return jsonify({
        "average_rating": average_rating,
        "review_count": result["review_count"],
        "reviews": [
            {
                "id": review["id"],
                "rating": review["rating"],
                "comment": review["comment"]
            }
            for review in reviews
        ]
    })