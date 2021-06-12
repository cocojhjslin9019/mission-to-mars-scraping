from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#set up
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#route
@app.route("/")
def index():
    mars_data_dict = mongo.db.mars_data_dict.find_one()
    return render_template("index.html", mars_data_dict = mars_data_dict)

@app.route("/scrape")
def scrape():
    mars_data_dict = mongo.db.mars_data_dict
    mars_data = scrape_mars.scrape()
    mars_data_dict.update({}, mars_data, upsert=True)
    return redirect("http://localhost:500/", code=302)

if __name__ == "__main__":
    app.run(debug=True)