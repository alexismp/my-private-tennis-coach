from flask import Flask, render_template, jsonify
import utils

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/five_principles")
def five_principles():
   return render_template("five-principles.html")

@app.route("/personal_analysis")
def personal_analysis():
   return render_template("analysis.html")

@app.route("/coaching_sources")
def coaching_sources():
   return render_template("coaching-sources.html")

@app.route("/get_coaching_sources")
def get_coaching_sources():
   json = utils.get_coaching_urls()
   print(json)
   return jsonify({'result': json}, 200, {'Content-Type': 'application/json'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
