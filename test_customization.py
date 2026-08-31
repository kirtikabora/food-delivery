from flask import Flask, render_template

app = Flask(__name__)


@app.route("/customize")
def customize():
    return render_template("customization.html")


if __name__ == "__main__":
    app.run(debug=True)