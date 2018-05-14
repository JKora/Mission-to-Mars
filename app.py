#import libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/scrape")
def scrape():
    mars_info_sets = mongo.db.mars_info_sets
    mars_info = scrape_mars.scrape()
    mars_info_sets.update(
        {},
        mars_info,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

# Route that renders index.html template
@app.route("/")
def home():
    mars_info_sets = mongo.db.mars_info_sets.find_one()
    return render_template("index.html", mars_info_sets=mars_info_sets)

if __name__ == "__main__":
    app.run(debug=True)