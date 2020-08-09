# Import dependencies.
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping_challenge

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo collection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")
def index_challenge():
    mars = mongo.db.mars.find_one()
    return render_template("index_challenge.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping_challenge.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()