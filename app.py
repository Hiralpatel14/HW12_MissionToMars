from flask import Flask, render_template, jsonify,redirect
from Flask_pymongo import Pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)
# Create connection variable
#conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
#client = pymongo.MongoClient(conn)

mongo = Pymongo(app)
# Set route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#scrap data and pull into mongo db

@app.route('/scrape')
def get():
    mars = mongo.db.mars
    marsdata = scrape_mars.scrape()
    mars.update({}, marsdata, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
        app.run(debug=True)