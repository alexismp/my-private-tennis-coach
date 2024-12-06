from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Placeholder for personal analysis page.  This would require more details about the intended functionality
@app.route("/personal_analysis")
def personal_analysis():
   return render_template("personal_analysis.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

